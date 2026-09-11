from fastapi import APIRouter

from app import analytics_findings as findings

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/type-breakdown")
def type_breakdown():
    return findings.TYPE_BREAKDOWN


@router.get("/speed-torque-region")
def speed_torque_region():
    return findings.SPEED_TORQUE_REGION


@router.get("/pwf-power-rule")
def pwf_power_rule():
    return findings.PWF_POWER_RULE


@router.get("/hdf-tempdiff")
def hdf_tempdiff():
    return findings.HDF_TEMPDIFF


@router.get("/osf-risk-index")
def osf_risk_index():
    return findings.OSF_RISK_INDEX
