import pytest

from meal_max.models.battle_model import BattleModel
from meal_max.models.kitchen_model import Meal
from unittest.mock import patch


@pytest.fixture()
def battle_model():
    """Fixture to provide a new instance of BattleModel for each test."""
    return BattleModel()

@pytest.fixture
def mock_update_meal_status(mocker):
    """Mock the update_meal_status function for testing purposes."""
    return mocker.patch("meal_max.models.kitchen_model.update_meal_status")


"""Fixtures providing sample meals for the tests."""
@pytest.fixture
def sample_meal1():
    return Meal(1, 'Steak', 'American', 40.50, 'HIGH')

@pytest.fixture
def sample_meal2():
    return Meal(2, 'Orange Chicken', 'Chinese', 18.00, 'MED')

@pytest.fixture
def sample_meal3():
    return Meal(3, 'Salad', 'Mediterranean', 15.00, 'LOW')

@pytest.fixture
def sample_combatants(sample_meal1, sample_meal2):
    return [sample_meal1, sample_meal2]

##################################################
# Combatant Management Test Cases
##################################################

def test_prep_combatant(battle_model, sample_meal1):
    """Test preparing one combatant"""
    battle_model.prep_combatant(sample_meal1)
    assert len(battle_model.combatants) == 1
    assert battle_model.combatants[0].meal == 'Steak'

def test_prep_two_combatants(battle_model, sample_meal1, sample_meal2):
    """Test preparing two combatants."""
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)
    assert len(battle_model.combatants) == 2

def test_prep_more_than_two_combatants(battle_model, sample_meal1, sample_meal2, sample_meal3):
    """Test error when trying to add a third combatant."""
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)
    with pytest.raises(ValueError, match="Combatant list is full, cannot add more combatants."):
        battle_model.prep_combatant(sample_meal3)

##################################################
# Battle Test Cases
##################################################

def test_battle_two_combatants(battle_model, sample_meal1, sample_meal2, mocker):
    """Test conducting a battle between two meals."""
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)

    mocker.patch("meal_max.models.battle_model.BattleModel.get_battle_score", side_effect = [85.5, 122.2])
    mocker.patch('meal_max.models.battle_model.get_random', return_value = 0.42)
    mock_update_meal_stats = mocker.patch('meal_max.models.battle_model.update_meal_stats')


    winner = battle_model.battle()
    assert winner in [sample_meal1.meal, sample_meal2.meal], "Winner should be one of the combatants"
    assert len(battle_model.get_combatants()) == 1, "One combatant should be removed after the battle"

    mock_update_meal_stats.assert_any_call(sample_meal1.id, 'win' if winner == sample_meal1.meal else 'loss')
    mock_update_meal_stats.assert_any_call(sample_meal2.id, 'win' if winner == sample_meal2.meal else 'loss')
    
def test_battle_not_enough_combatants(battle_model):
    """Test error when trying to battle with fewer than two combatants."""
    with pytest.raises(ValueError, match="Two combatants must be prepped for a battle."):
        battle_model.battle()

##################################################
# Combatant Management Test Cases
##################################################

def test_clear_combatants(battle_model, sample_meal1):
    """Test clearing the combatants list."""
    battle_model.prep_combatant(sample_meal1)
    battle_model.clear_combatants()
    assert len(battle_model.get_combatants()) == 0, "Combatants list should be empty after clearing"

def test_clear_empty_combatants(battle_model, caplog):
    """Test clearing an already empty combatants list and check logging."""
    battle_model.clear_combatants()
    assert len(battle_model.get_combatants()) == 0, "Combatants list should be empty after clearing"
    assert "Clearing the combatants list." in caplog.text, "Expected log message when clearing combatants list"

##################################################
# Battle Score Calculation Test Cases
##################################################

def test_get_battle_score(battle_model, sample_meal1):
    """Test calculating battle score for a combatant."""
    score = battle_model.get_battle_score(sample_meal1)
    expected_score = (sample_meal1.price * len(sample_meal1.cuisine)) - 1  # MED difficulty modifier = 2
    assert score == expected_score, f"Expected score {expected_score}, but got {score}"

def test_get_battle_score_with_different_difficulty(battle_model, sample_meal2):
    """Test battle score calculation with a different difficulty level."""
    score = battle_model.get_battle_score(sample_meal2)
    expected_score = (sample_meal2.price * len(sample_meal2.cuisine)) - 2  # LOW difficulty modifier = 3
    assert score == expected_score, f"Expected score {expected_score}, but got {score}"