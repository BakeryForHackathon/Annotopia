from utils.get_randam_test_id import get_unanswered_test_ids

def is_test_ended(user_id, task_id):
    """
    指定されたユーザーとタスクに対して、テストが終了しているかどうかを判定する。
    終了条件は、未回答のテストデータが存在しないこと。
    """
    unanswered_ids = get_unanswered_test_ids(user_id, task_id)
    return len(unanswered_ids) == 0