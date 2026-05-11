import requests


class ApiReader:
    _MAX_ITEMS = 100
    _FIELDS = (
        "budget_fiscal_year",
        "appr",
        "appropriation",
        "expenditure_classification",
        "current_budget",
        "encumbrance",
        "expenses",
    )

    def __init__(self, url, timeout_seconds=20):
        self._url = url
        self._timeout = timeout_seconds

    def read(self):
        response = requests.get(self._url, timeout=self._timeout)
        response.raise_for_status()
        data = response.json()
        return self._normalize(data)

    def _normalize(self, data):
        if isinstance(data, list):
            items = [self._select_fields(item) for item in data if isinstance(item, dict)]
            return items[: self._MAX_ITEMS]
        if isinstance(data, dict):
            if "data" in data and isinstance(data["data"], list):
                items = [
                    self._select_fields(item)
                    for item in data["data"]
                    if isinstance(item, dict)
                ]
                return items[: self._MAX_ITEMS]
            return [self._select_fields(data)]
        raise ValueError("API response must be a JSON object or array.")

    def _select_fields(self, item):
        return {field: item.get(field) for field in self._FIELDS}
