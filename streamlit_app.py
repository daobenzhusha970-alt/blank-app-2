import streamlit as st
from supabase import create_client

# Supabase 接続
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

st.title("📝 Supabase Todo アプリ")

# ------------------------
# Todo 追加
# ------------------------
st.subheader("Todoを追加")

with st.form("add_todo"):
    title = st.text_input("Todo内容")
    submitted = st.form_submit_button("追加")

    if submitted and title:
        supabase.table("todos").insert({
            "title": title
        }).execute()
        st.success("Todoを追加しました")

# ------------------------
# Todo 一覧表示
# ------------------------
st.subheader("Todo一覧")

todos = supabase.table("todos").select("*").order("created_at").execute()

if todos.data:
    for todo in todos.data:
        col1, col2 = st.columns([3, 1])

        with col1:
            checked = st.checkbox(
                todo["title"],
                value=todo["is_done"],
                key=todo["id"]
            )

            if checked != todo["is_done"]:
                supabase.table("todos") \
                    .update({"is_done": checked}) \
                    .eq("id", todo["id"]) \
                    .execute()

        with col2:
            if st.button("🗑 削除", key=f"del_{todo['id']}"):
                supabase.table("todos") \
                    .delete() \
                    .eq("id", todo["id"]) \
                    .execute()
                st.experimental_rerun()
else:
    st.write("Todoはまだありません")

