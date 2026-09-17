


def create_word(supabase, wordset_id,word,english):
    response = (
        supabase
        .table("words")
        .insert({
            "wordset_id":wordset_id,
            "word":word,
            "english":english
        })
        .execute()
    )
    return response.data

def get_words(supabase,wordset_id):
    response = (
        supabase
        .table("words")
        .select("*")
        .eq("wordset_id",wordset_id)
        .execute()
    )

    return response.data

def update_word(supabase,wordset_id,word_id,word = None, english = None):
    updates = {}

    if word is not None:
        updates["word"] = word
    if english is not None:
        updates["english"] = english

    response = (
        supabase
        .table("words")
        .update(updates)
        .eq("id",word_id)
        .eq("wordset_id",wordset_id)
        .execute()
    )

    if not response.data:
        return None

    return response.data

def delete_word(supabase,wordset_id,word_id):
    response = (
        supabase
        .table("words")
        .delete()
        .eq("wordset_id",wordset_id)
        .eq("id",word_id)
        .execute()
    )
    if not response.data:
        return None
    return response.data
