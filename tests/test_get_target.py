from apps.testing.calculator.target import get_target, SPA_TARGET, TRADITIONAL_POOL_TARGET
from core.constants import Chemistry, POOL_TYPE_SPA, POOL_TYPE_POOL, POOL_SURFACE_PLASTER, CHLORINE_SOURCE_BLEACH


def test_chemistry_read():
    target = get_target(POOL_TYPE_SPA, None, None)
    assert id(target) == id(SPA_TARGET)
    assert target == SPA_TARGET

    target = get_target(POOL_TYPE_POOL, None, None)

    assert id(target) != id(TRADITIONAL_POOL_TARGET)
    assert target == TRADITIONAL_POOL_TARGET

    target = get_target(POOL_TYPE_POOL, POOL_SURFACE_PLASTER, CHLORINE_SOURCE_BLEACH)
