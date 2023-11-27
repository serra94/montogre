import pytest

from project.resources.data_generator import (
    generator_client_data,
    generator_delivery_data,
    generator_driver_data,
    generator_location_data,
    generator_product_data,
    generator_vehicle_data,
)

GENERATING_FUNCTIONS = [
    generator_driver_data,
    generator_vehicle_data,
    generator_client_data,
    generator_delivery_data,
    generator_location_data,
    generator_product_data,
]


@pytest.mark.parametrize('generate_function', GENERATING_FUNCTIONS)
def test_generate_data_result_and_single_key_value_pair(generate_function):
    result = generate_function()
    assert isinstance(result, dict) and len(result) == 1


@pytest.mark.parametrize(
    'generate_function, quantity', [(func, 2) for func in GENERATING_FUNCTIONS]
)
def test_generate_data_value_is_list_with_correct_length(
    generate_function, quantity
):
    result = generate_function(quantity=quantity)
    key = list(result.keys())[0]
    value = result[key]
    assert isinstance(value, list) and len(value) == quantity


@pytest.mark.parametrize(
    'generate_function, quantity',
    [(func, None) for func in GENERATING_FUNCTIONS],
)
def test_generate_data_with_none_quantity(generate_function, quantity):
    with pytest.raises(ValueError):
        generate_function(quantity=quantity)


@pytest.mark.parametrize(
    'generate_function, quantity', [(func, 0) for func in GENERATING_FUNCTIONS]
)
def test_generate_data_with_zero_quantity(generate_function, quantity):
    with pytest.raises(ValueError):
        generate_function(quantity=quantity)


@pytest.mark.parametrize(
    'generate_function, quantity',
    [(func, 'str') for func in GENERATING_FUNCTIONS],
)
def test_generate_data_with_string_quantity(generate_function, quantity):
    with pytest.raises(ValueError):
        generate_function(quantity=quantity)


@pytest.mark.parametrize(
    'generate_function, collection_name',
    [(func, 'TestCollection') for func in GENERATING_FUNCTIONS],
)
def test_generate_data_change_collection_name(
    generate_function, collection_name
):
    result = generate_function(collection_name=collection_name)
    key = list(result.keys())[0]
    assert key == collection_name
