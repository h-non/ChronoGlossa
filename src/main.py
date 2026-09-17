from fastapi import FastAPI,Depends,HTTPException
from pydantic import BaseModel
from src.auth import get_current_user
from src.wordsets import create_wordset,update_wordset,delete_wordset
from src.words import create_word,get_words,update_word,delete_word
from src.mastery import create_mastery,update_user_mastery,get_user_mastery,get_wordset_mastery,get_practice_words
from src.sessions import create_session,end_session,get_sessions,get_session






app = FastAPI()

class WordsetCreate(BaseModel):
    name: str
    language: str
    is_public: bool = False
class MasteryAnswer(BaseModel):
    correct : bool
@app.get("/me")
def get_my_profile(
    auth = Depends(get_current_user)
):
    user,supabase = auth

    response = (
        supabase
        .table("users")
        .select("*")
        .eq("id",user.id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )
    return response.data[0]
@app.patch("/wordsets/{wordset_id}")
def update_existing_wordset(
    wordset_id: int,
    wordset:WordsetCreate,
    auth=Depends(get_current_user)
):
    user,supabase = auth
    result = update_wordset(
        supabase,
        wordset_id,
        wordset.name,
        wordset.language,
        wordset.is_public
    )
    if not  result: raise HTTPException(
        status_code=404,
        detail="Wordset not found or you are not allowed to access it."

    )
        

    return result


@app.post("/wordsets")
def create_new_wordset(
    wordset:WordsetCreate,
    auth=Depends(get_current_user)
):
    user,supabase = auth

    return create_wordset(
        supabase,
        user,
        wordset.name,
        wordset.language,
        wordset.is_public
    )


@app.get("/wordsets")
def get_wordsets(auth=Depends(get_current_user)):
    user,supabase = auth

    response = (
        supabase
        .table("wordsets")
        .select("*")
        .execute()
    )

    return response.data
@app.delete("/wordsets/{wordset_id}")
def delete_existing_wordset(
    wordset_id: int,
    auth=Depends(get_current_user)
):
    user,supabase = auth

    result = delete_wordset(
        supabase,
        wordset_id
    )

    if not result: raise HTTPException(
        status_code=404,
        detail="Wordset not found or you are not allowed to access it."
    )


    return result

class WordCreate(BaseModel):
    word : str
    english: str
@app.post("/wordsets/{wordset_id}/words")
def create_new_word(
    wordset_id : int,
    word : WordCreate,
    auth=Depends(get_current_user)
):
    user,supabase = auth
    return create_word(
        supabase,
        wordset_id,
        word.word,
        word.english
    )

@app.get("/wordsets/{wordset_id}/words")
def get_wordset_words(
    wordset_id : int,
    auth=Depends(get_current_user)
):
    user, supabase = auth

    return get_words(
        supabase,
        wordset_id
    )
@app.patch("/wordsets/{wordset_id}/words/{word_id}")
def update_wordset_word(
    wordset_id : int,
    word_id : int,
    word : WordCreate,
    auth = Depends(get_current_user)
):
    user,supabase = auth
    result = update_word(
        supabase,
        wordset_id,
        word_id,
        word.word,
        word.english
    )
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Word not found or you are not allowed to access it."
        )
    return result

@app.delete("/wordsets/{wordset_id}/words/{word_id}")
def delete_existing_word(
    wordset_id: int,
    word_id: int,
    auth=Depends(get_current_user)
):
    user, supabase = auth



    result = delete_word(
        supabase,
        wordset_id,
        word_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Word not found or you are not allowed to access it."
        )

    return result

@app.post("/wordsets/{wordset_id}/words/{word_id}/mastery")
def create_word_mastery(
     wordset_id : int,
     word_id : int,
     auth = Depends(get_current_user)
):
    user,supabase = auth

    word_response = (
            supabase
            .table("words")
            .select("id")
            .eq("id",word_id)
            .eq("wordset_id",wordset_id)
            .execute()
        )
    if not word_response.data:
            raise HTTPException(
                status_code=404,
                detail="Word not found"
            )
    return create_mastery(
        supabase,
        user,
        wordset_id,
        word_id

    )

@app.patch("/wordsets/{wordset_id}/words/{word_id}/mastery")
def update_existing_mastery(
    wordset_id : int,
    word_id : int,
    answer : MasteryAnswer,
    auth = Depends(get_current_user)
):    
    user, supabase = auth

    result = update_user_mastery(
        supabase,
        user,
        wordset_id,
        word_id,
        answer.correct
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Mastery record or word not found"
        )

    return result

@app.get("/wordsets/{wordset_id}/words/{word_id}/mastery")

def get_mastery(
    word_id : int,
    wordset_id : int,
    auth = Depends(get_current_user)
):
    user,supabase = auth

    word_response = (
        supabase
        .table("words")
        .select("id")
        .eq("id", word_id)
        .eq("wordset_id",wordset_id)
        .execute()
    )

    if not word_response.data:
        raise HTTPException(
            status_code=404,
            detail="Word not found or you dont have access to the word."
        )
           

    result = get_user_mastery(supabase,user,word_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Mastery record not found"
        )
    
    return result

@app.get("/wordsets/{wordset_id}/mastery")

def see_wordset_mastery(
    wordset_id : int,
    auth = Depends(get_current_user)
):
    user,supabase = auth

    result = get_wordset_mastery(supabase,user,wordset_id)

    return result

@app.post("/sessions")
def start_session(
    auth = Depends(get_current_user)
):
    user,supabase = auth

    return create_session(
        supabase,
        user
    )

@app.patch("/sessions/{session_id}")
def finish_session(
    session_id : int,
    auth = Depends(get_current_user)
):
    user,supabase = auth

    result = end_session(supabase,user,session_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Sesssion not found or it's inaccesible to you"
        )

    return result

@app.get("/sessions")
def get_user_sessions(
    auth = Depends(get_current_user)
):
    user,supabase = auth

    return get_sessions(
        supabase,
        user
    )

@app.get("/sessions/{session_id}")

def get_sesssion_duration(
    session_id : int,
    auth = Depends(get_current_user)
):
    user,supabase = auth

    result = get_session(
        supabase,
        user,
        session_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="This session data doesn't exist or you dont have access"
        )

    return result
@app.get("/wordsets/{wordset_id}/practice")
def get_practice(
    wordset_id : int,
    auth = Depends(get_current_user)

):
    user,supabase= auth

    return get_practice_words(
        supabase,
        user,
        wordset_id
    )