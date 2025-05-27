from datetime import date, timedelta, datetime

import pytest
from pydantic import ValidationError

from app.schemas.get_dynamics_params import GetDynamicsParamsSchema, GetDynamicsParamsDateIntervalSchema


class TestGetDynamicsParamsSchema:
    """Тесты для GetDynamicsParamsSchema"""

    def test_valid_data(self):
        # Проверка с корректными данными
        data = {
            "oil_id": "BRN",
            "delivery_type_id": "F",
            "delivery_basis_id": "AAA"
        }
        schema = GetDynamicsParamsSchema(**data)
        assert schema.oil_id == "BRN"
        assert schema.delivery_type_id == "F"
        assert schema.delivery_basis_id == "AAA"

    def test_null_values(self):
        # Проверка, что все поля могут быть None
        data = {}
        schema = GetDynamicsParamsSchema(**data)
        assert schema.oil_id is None
        assert schema.delivery_type_id is None
        assert schema.delivery_basis_id is None

    @pytest.mark.parametrize(
        "field, value",
        [
            ("oil_id", "BRENT"),  # Слишком длинный oil_id
            ("delivery_type_id", "FF"),  # Слишком длинный delivery_type_id
            ("delivery_basis_id", "AAAA"),  # Слишком длинный delivery_basis_id
        ]
    )
    def test_max_length_validation(self, field, value):
        # Проверка валидации максимальной длины
        with pytest.raises(ValidationError) as exc_info:
            data = {field: value}
            GetDynamicsParamsSchema(**data)

        assert "string_too_long" in [str(error.get('type')) for error in
                                     exc_info.value.errors()]


class TestGetDynamicsParamsDateIntervalSchema:
    """Тесты для схемы с интервалом дат"""

    @pytest.mark.parametrize(
        "start_date, end_date, expected_error",
        [
            # Будущая start_date
            (
                    (datetime.now() + timedelta(days=10)).date().isoformat(),
                    (datetime.now() + timedelta(days=12)).date().isoformat(),
                    "Нельзя запрашивать данные из будущего"
            ),
            # Будущая end_date
            (
                    "2023-01-01",
                    (datetime.now() + timedelta(days=10)).date().isoformat(),
                    "Нельзя запрашивать данные из будущего"
            ),
            # start_date > end_date
            (
                    "2023-02-01",
                    "2023-01-01",
                    "Начальная дата не может быть больше конечной"
            ),
            # Корректные даты (без ошибки)
            (
                    "2023-01-01",
                    "2023-01-10",
                    None
            ),
        ],
        ids=[
            "future_start_date",
            "future_end_date",
            "start_after_end",
            "valid_dates",
        ]
    )
    def test_date_validation(self, start_date, end_date, expected_error):
        # Проверка разных слочетаний дат
        data = {
            "start_date": start_date,
            "end_date": end_date,
        }

        if expected_error:
            with pytest.raises(ValidationError) as exc_info:
                GetDynamicsParamsDateIntervalSchema(**data)

            # Проверяем, что ожидаемая ошибка содержится в сообщении об ошибке
            errors = [str(error.get('ctx').get('error')) for error in exc_info.value.errors()]
            assert expected_error in errors
        else:
            # Для валидных данных проверяем корректное создание схемы
            schema = GetDynamicsParamsDateIntervalSchema(**data)
            assert schema.start_date == date.fromisoformat(start_date)
            assert schema.end_date == date.fromisoformat(end_date)

    @pytest.mark.parametrize(
        "date_str",
        [
            "invalid-date",
            "2023-13-01",  # Неверный месяц
            "2023-02-30",  # Неверный день
            "23-01-01",  # Неверный формат года
        ]
    )
    def test_invalid_date_format(self, date_str):
        # Неверный формат даты
        with pytest.raises(ValidationError):
            data = {
                "start_date": date_str,
                "end_date": "2023-01-01",
            }
            GetDynamicsParamsDateIntervalSchema(**data)
