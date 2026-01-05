import json
import sys
import re
import pandas as pd


def parse_jsonl(file_name):
    lines = open(file_name).readlines()
    return [json.loads(line) for line in lines]


def unwrap_answer(data):
    if isinstance(data, dict) and "answer" in data:
        return data["answer"]
    return data


def extract_json_content(text):
    if not text:
        return None
    
    text = text.strip()
    start = text.find('{')
    end = text.rfind('}') + 1
    if start == -1 or end <= start:
        return None

    try:
        return json.loads(text[start:end])
    except json.JSONDecodeError:
        return None


def normalize_val(val):
    if val is None:
        return ""
    s = re.sub(r"[<>]", "", str(val)).strip()
    if not s:
        return ""
    num_candidate = s.replace(",", "")
    try:
        num = float(num_candidate)
    except ValueError:
        return s
    return str(int(num)) if num.is_integer() else str(num)


def flatten_json(data, prefix=""):
    items = set()
    if isinstance(data, dict):
        for k, v in data.items():
            items.update(flatten_json(v, f"{prefix}.{k}" if prefix else k))
    elif isinstance(data, list):
        for v in data:
            if isinstance(v, list):
                row_tuple = tuple(normalize_val(sub_item) for sub_item in v)
                items.add((prefix, row_tuple))
            else:
                items.update(flatten_json(v, prefix))
    else:
        s = normalize_val(data)
        parts = re.split(r'[，,]', s)
        for part in parts:
            part = part.strip()
            if part:
                items.add((prefix, part))
    return items


def calculate_metrics(pred_json, gt_json, doc_id=None):
    def filter_present_categories(obj):
        return {"present_categories": obj.get("present_categories", [])} if isinstance(obj, dict) else {}

    if doc_id and doc_id.startswith("DTR_003"):
        pred_json = filter_present_categories(pred_json)
        gt_json = filter_present_categories(gt_json)

    if doc_id and (doc_id.startswith("NC_001") or doc_id.startswith("NC_002")):
        if pred_json is None:
            return None
        try:
            return 1.0 if abs(float(pred_json) - float(gt_json)) <= 2 else 0.0
        except Exception:
            return 0.0

    pred_set = flatten_json(pred_json) if pred_json is not None else set()
    gt_set = flatten_json(gt_json)

    if not gt_set:
        return 1.0 if not pred_set else 0.0

    tp = len(pred_set & gt_set)
    fp = len(pred_set) - tp
    fn = len(gt_set) - tp

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0.0
    return f1


def evaluate_samples(pred_file, gt_file):
    predictions = parse_jsonl(pred_file)
    gts = parse_jsonl(gt_file)
    gt_map = {gt['id']: gt for gt in gts}
    raw_scores = []
    for pred_data in predictions:
        doc_id = pred_data['id']
        # task NC_005 is currently under construction
        if doc_id.startswith('NC_005'): 
            continue
        pred_json = extract_json_content(pred_data['response'])
        gt_json = json.loads(gt_map[doc_id]['response'])
        pred_json = unwrap_answer(pred_json)
        gt_json = unwrap_answer(gt_json)
        
        f1 = calculate_metrics(pred_json, gt_json, doc_id)
        raw_score = {
            "id": doc_id,
            "task": gt_map[doc_id]['task'],
            "subtask": gt_map[doc_id]['subtask'],
            "robustness": gt_map[doc_id]['robustness'],
            "f1": f1
        }
        raw_scores.append(raw_score)
    return raw_scores


def evaluate_tasks(raw_scores):
    df = pd.DataFrame(raw_scores)
    subtask_mean = (
    df.groupby(["task", "subtask"], as_index=False)
        .agg(subtask_f1_mean=("f1", "mean"))
    )
    task_mean = (
        subtask_mean.groupby("task", as_index=False)
                    .agg(task_f1=("subtask_f1_mean", "mean"))
    )
    order = ["DTR", "KIE", "IQE", "CC", "VC", "NC", "RR"] 
    task_mean_sorted = (
        task_mean.assign(task=pd.Categorical(task_mean["task"], categories=order, ordered=True))
                .sort_values("task")
                .reset_index(drop=True)
    )
    print("Performance by Task:\n", task_mean_sorted)
    return task_mean_sorted['task_f1'].mean()


def evaluate_robustness(raw_scores):
    df = pd.DataFrame(raw_scores)
    subtask_mean = (
        df.loc[df["task"].ne("IQE")]
        .groupby(["robustness", "task", "subtask"], as_index=False)
        .agg(subtask_f1_mean=("f1", "mean"))
    )
    normal_sub_mean = (
        subtask_mean[subtask_mean["robustness"].eq("Normal Captures")]
    )
    normal_task_mean = (
        normal_sub_mean.groupby("task", as_index=False)
                .agg(task_f1=("subtask_f1_mean", "mean"))
    )
    normal_overall_mean = normal_task_mean["task_f1"].mean()

    sec_keys = (
        subtask_mean.loc[subtask_mean["robustness"].eq("Secondary Captures"), ["task", "subtask"]]
                .drop_duplicates()
    )
    sec_normal_sub_mean = (
        subtask_mean[subtask_mean["robustness"].eq("Normal Captures")]
        .merge(sec_keys, on=["task", "subtask"], how="inner")
    )
    sec_normal_task_mean = (
        sec_normal_sub_mean.groupby("task", as_index=False)
                    .agg(task_f1=("subtask_f1_mean", "mean"))
    )
    sec_normal_overall_mean = sec_normal_task_mean["task_f1"].mean()
    
    multi_subtask_mean = (
        df.loc[df["subtask"].isin([
            "DTR_001_001", 
            "DTR_003_001",
            "KIE_002_001",
            ])]  
        .groupby(["robustness", "task", "subtask"], as_index=False)
        .agg(subtask_f1_mean=("f1", "mean"))
    )

    multi_normal_sub_mean = (
        multi_subtask_mean[multi_subtask_mean["robustness"].eq("Normal Captures")]
    )
    multi_normal_task_mean = (
        multi_normal_sub_mean.groupby("task", as_index=False)
                    .agg(task_f1=("subtask_f1_mean", "mean"))
    )
    multi_normal_overall_mean = multi_normal_task_mean["task_f1"].mean()

    task_mean = (
        subtask_mean.groupby(["robustness", "task"], as_index=False)
                    .agg(task_f1=("subtask_f1_mean", "mean"))
    )
    robustness_scores = (
        task_mean.groupby("robustness", as_index=False)
                 .agg(robustness_macro_f1=("task_f1", "mean"))
                 .sort_values("robustness_macro_f1", ascending=False)
                 .reset_index(drop=True)
    )
    use_special_denoms = {
        "Secondary Captures": sec_normal_overall_mean,
        "Cluttered Background": sec_normal_overall_mean,
        "Multi-doc Images": multi_normal_overall_mean}  
    robustness_scores = robustness_scores.copy()
    robustness_scores["normal_denom"] = robustness_scores["robustness"].apply(
        lambda r: use_special_denoms.get(r, normal_overall_mean)
    )
    robustness_scores["relative_to_normal"] = (
        robustness_scores["robustness_macro_f1"] / robustness_scores["normal_denom"]
    )
    robustness_scores = robustness_scores.drop(columns=["normal_denom", "robustness_macro_f1"])
    robustness_scores = robustness_scores.sort_values('relative_to_normal', ascending=False)
    print("Performance by Robustness:\n", robustness_scores)


if __name__ == "__main__":
    p_file = sys.argv[1]
    g_file = sys.argv[2]
    raw_scores = evaluate_samples(p_file, g_file)
    evaluate_tasks(raw_scores)
    evaluate_robustness(raw_scores)
