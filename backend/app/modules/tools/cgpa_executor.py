class CGPAExecutor:

    def execute(self, data):

        grades = data.get("grades", [])

        if not grades:
            raise ValueError("No grades provided")

        cgpa = sum(grades) / len(grades)

        return {
            "cgpa": round(cgpa, 2)
        }