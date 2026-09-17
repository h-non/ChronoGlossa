from datetime import datetime


def create_session(supabase,user):
    response = (
        supabase
        .table("sessions")
        .insert({
            "user_id": user.id
        })
        .execute()
    )

    return response.data

def end_session(supabase,user,session_id):
    response = (
        supabase
        .table("sessions")
        .update({
            "ended_at": "now()"
        })
        .eq("id",session_id)
        .eq("user_id",user.id)
        .execute()
    )

    if not response.data:
        return None

    return response.data

def get_sessions(supabase,user):
    response = (
        supabase
        .table("sessions")
        .select("*")
        .eq("user_id", user.id)
        .execute()
    )
    return response.data

def get_session(supabase,user,session_id):
    response = (
        supabase
        .table("sessions")
        .select("*")
        .eq("id",session_id)
        .eq("user_id",user.id)
        .execute()
    )

    if not response.data:
        return None

    session = response.data[0]

    if session["ended_at"] is not None:
        started = datetime.fromisoformat(session["started_at"])
        ended = datetime.fromisoformat(session["ended_at"])


        session["duration"] = (ended - started).total_seconds()
    else:
        session["duration"] = None

    return session