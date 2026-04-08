#app/domain/profile_domain.py
from datetime import datetime, timedelta


class ProfileDomain:

    @staticmethod
    def calculate_account_age(created_at):
        if not created_at:
            return 0

        now = datetime.utcnow()
        return (now - created_at).days

    @staticmethod
    def build_performance_history(xp_rows):
        xp_map = {str(row[0]): int(row[1]) for row in xp_rows}

        today = datetime.utcnow().date()

        return [
            {
                "day": (today - timedelta(days=i)).strftime("%a").upper(),
                "xp": xp_map.get(str(today - timedelta(days=i)), 0)
            }
            for i in range(6, -1, -1)
        ]