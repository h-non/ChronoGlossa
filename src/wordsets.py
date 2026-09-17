


def create_wordset(supabase,user,name,language,is_public=False):
    response = (
        supabase
        .table("wordsets")
        .insert({
            "user_id":user.id,
            "name":name,
            "language":language,
            "is_public":is_public
        })
        .execute()
    )
    return response.data

def get_my_wordsets(supabase):
    response = supabase.table("wordsets").select("*").execute()

    return response.data

def update_wordset(supabase, wordset_id,name=None,language=None,is_public=None):

    updates = {}

    if name is not None:
        updates["name"] = name

    if language is not None:
        updates["language"] = language

    if is_public is not None:
        updates["is_public"]=is_public

    response = (
        supabase
        .table("wordsets")
        .update(updates)
        .eq("id",wordset_id)
        .execute()
    )

    if response.data is None:
        return None

    return response.data


def delete_wordset(supabase,wordset_id):
    response = (
        supabase
        .table("wordsets")
        .delete()
        .eq("id",wordset_id)
        .execute()
    )
    if response.data is None:
        return None
    return response.data
