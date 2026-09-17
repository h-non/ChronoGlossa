from datetime import datetime

def create_mastery(supabase,user,wordset_id,word_id):

    word_response = (
        supabase
        .table("words")
        .select("id")
        .eq("id", word_id)
        .eq("wordset_id", wordset_id)
        .execute()
    )

    if not word_response.data:
        return None

    existing = (
        supabase
        .table("mastery")
        .select("*")
        .eq("user_id", user.id)
        .eq("word_id", word_id)
        .execute()
    )

    if existing.data:
        return existing.data

    response = (
        supabase
        .table("mastery")
        .insert({
            "user_id" : user.id,
            "word_id" : word_id
        })
        .execute()
        )
    return response.data


def update_user_mastery(supabase,user,wordset_id,word_id,correct):
    word_response= (
        supabase
        .table("words")
        .select("id")
        .eq("id",word_id)
        .eq("wordset_id",wordset_id)
        .execute()
    )

    if not word_response.data:
        return None

    mastery_response = (
        supabase
        .table("mastery")
        .select("*")
        .eq("user_id",user.id)
        .eq("word_id",word_id)
        .execute()
    )
    
    if not mastery_response.data:
        return None

    mastery = mastery_response.data[0]
    current_mastery = float(mastery["mastery"])
    attempts = mastery["attempts"]

    if correct:
        current_mastery += 10
    else:
        current_mastery -= 10

    current_mastery = max(0, min(100, current_mastery))

    response = (
        supabase
        .table("mastery")
        .update({
            "mastery": current_mastery,
            "attempts": attempts + 1,
            "last_seen": datetime.now().astimezone().isoformat()
        })
        .eq("user_id", user.id)
        .eq("word_id", word_id)
        .execute()
    )

    return response.data

def get_user_mastery(supabase,user,word_id):
    response = (
        supabase
        .table("mastery")
        .select("*")
        .eq("user_id",user.id)
        .eq("word_id",word_id)
        .execute()
        )
    return response.data

def get_wordset_mastery(supabase,user,wordset_id):
    word_response = (
        supabase
        .table("words")
        .select("id")
        .eq("wordset_id",wordset_id)
        .execute()
    )

    if not word_response.data:
        return []

    word_ids = [word["id"] for word in word_response.data]

    response = (
        supabase
        .table("mastery")
        .select("*")
        .eq("user_id",user.id)
        .in_("word_id",word_ids)
        .execute()
    )

    return response.data

def get_practice_words(supabase,user,wordset_id):
    word_response = (
        supabase
        .table("words")
        .select("*")
        .eq("wordset_id",wordset_id)
        .execute()
    )

    if not word_response.data:
        return []

    word_ids = [word["id"] for word in word_response.data]

    mastery_response = (
        supabase
        .table("mastery")
        .select("*")
        .eq("user_id",user.id)
        .in_("word_id",word_ids)
        .execute()
    )

    mastery_map = {
        mastery["word_id"]: mastery
        for mastery in mastery_response.data
    }

    practice_words = []

    for word in word_response.data:
        mastery = mastery_map.get(word["id"])

        if mastery:
            practice_words.append({
                "id": word["id"],
                "word": word["word"],
                "english": word["english"],
                "mastery": mastery["mastery"],
                "last_seen": mastery["last_seen"]
            })
        else:
            practice_words.append({
                "id": word["id"],
                "word": word["word"],
                "english": word["english"],
                "mastery": 0,
                "last_seen": None
            })
    practice_words.sort(
            key=lambda word:(
                word["mastery"],
                word["last_seen"] is not None,
                word["last_seen"] or ""

            )
        )
    return practice_words