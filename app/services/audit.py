from app.models.audit_log import AuditLog


def write_audit_log(
    db,
    username,
    action,
    entity_type,
    entity_id,
    details
):

    log = AuditLog()

    log.username = username

    log.action = action

    log.entity_type = entity_type

    log.entity_id = entity_id

    log.details = details

    db.add(log)

    db.commit()