def pc_schema(pc) -> dict:
    return {"id": str(pc["_id"]),
            "name": pc["name"],
            "ip": pc["ip"],
            "ping": pc["ping"],
            "count": pc["count"]}

def pcs_schema(pcs) -> list:
    return [pc_schema(pc) for pc in pcs]