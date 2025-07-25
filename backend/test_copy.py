from utils.get_ids import get_ids_by_task_id
from utils.get_requests import get_questions_by_task
from utils.set_test_data import set_test_data
from utils.has_copied_test_data import has_copied_test_data_any  # ← コピー済み判定関数をインポート

def test_copy(task_id, user_id):
    try:
        # 既にコピーされていたら何もせず成功として返す
        if has_copied_test_data_any(user_id, task_id):
            print("既にコピーされています。")
            return {
                "task_id": task_id,
                "user_id": user_id,
                "success": True,
                "message": "すでにコピー済みです。"
            }

        test_ids = get_ids_by_task_id(task_id, "test_data")
        if not test_ids:
            print("エラー: test_data が見つかりませんでした。")
            return {
                "task_id": task_id,
                "user_id": user_id,
                "success": False,
                "message": "test_data が見つかりませんでした。"
            }

        requests = get_questions_by_task(task_id)
        if not requests:
            print("エラー: 質問データが見つかりませんでした。")
            return {
                "task_id": task_id,
                "user_id": user_id,
                "success": False,
                "message": "質問データが見つかりませんでした。"
            }

        set_test_data(test_ids, user_id, len(requests))
        return {
            "task_id": task_id,
            "user_id": user_id,
            "success": True,
            "message": "コピーに成功しました。"
        }
    except Exception as e:
        print(f"test_copy中にエラーが発生しました: {e}")
        return {
            "task_id": task_id,
            "user_id": user_id,
            "success": False,
            "message": f"エラー: {e}"
        }