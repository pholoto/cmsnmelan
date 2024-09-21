import streamlit as st

# Section 1: MCQs Questions about Self
def mcq_section(questions, answers_by_child):
    st.header("Vòng 1: Ai hiểu mẹ Lan nhất?!")

    current_question = st.session_state.current_question

    # Display the current question
    if current_question < len(questions):
        st.write(f"Câu {current_question + 1}: {questions[current_question]}")
        
        # Display the answer options from each contestant
        options = [f"{name}: {answer}" for name, answer in answers_by_child[current_question].items()]
        selected_options = st.multiselect(f"Mẹ hãy chọn câu trả lời đúng nhất cho Câu {current_question + 1} (có thể chọn nhiều hơn một):", options, key=f"q_{current_question}")
        
        # Only show "Tiếp tục" if at least one option is selected
        if selected_options and st.button("Câu tiếp theo"):
            # Update scores based on the selected options
            for selected_option in selected_options:
                child_name = selected_option.split(":")[0]
                st.session_state.scores[child_name] += 1
            
            # Move to the next question
            st.session_state.current_question += 1
    else:
        st.write("Vòng 1 đã hoàn thành!")

# Section 2: MCQs for Photos (Guessing event/year)
def photo_mcq_section(photos, guesses_by_child):
    st.header("Vòng 2: Nhìn hình đoán địa điểm")

    current_photo = st.session_state.current_photo

    # Display the current photo and its question
    if current_photo < len(photos):
        photo_url, question = list(photos.items())[current_photo]
        st.write(f"Ảnh {current_photo + 1}: {question}")
        st.image(photo_url, use_column_width=True)
        
        # Display the guessing options
        options = [f"{name}: {guess}" for name, guess in guesses_by_child[current_photo].items()]
        selected_options = st.multiselect(f"Mẹ hãy chọn câu trả lời đúng nhất cho Ảnh {current_photo + 1} (có thể chọn nhiều hơn một):", options, key=f"photo_{current_photo}")
        
        # Only show "Tiếp tục" if at least one option is selected
        if selected_options and st.button("Câu tiếp theo"):
            # Update scores based on the selected options
            for selected_option in selected_options:
                child_name = selected_option.split(":")[0]
                st.session_state.scores[child_name] += 1
            
            # Move to the next photo
            st.session_state.current_photo += 1
    else:
        st.write("Vòng 2 đã hoàn thành!")

# Section 3: Sharing Videos and Memories (No scoring here)
def memory_section(children_videos):
    st.header("Vòng 3: Lời chúc từ cả nhà")

    # Tabs for each child
    tabs = st.tabs([f"Lời chúc của {child}" for child in children_videos.keys()])
    
    for i, (child, video_url) in enumerate(children_videos.items()):
        with tabs[i]:
            st.write(f"Lời chúc của {child}")
            st.video(video_url)
            st.write(f"Lời chúc của {child}!")

# Section to display the final scores and show top 3 participants
def score_conclusion_section():
    st.header("Kết quả vòng thi!")
    
    # Sort the scores in descending order to get top 3 and lowest 3
    sorted_scores = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
    
    # Top 3 participants
    top_3 = sorted_scores[:3]
    
    # Lowest 3 participants
    lowest_3 = sorted(sorted_scores, key=lambda x: x[1])[:3]

    # Display the top 3 participants
    st.write("🎉 **Cảm ơn cả nhà đã tham gia trò chơi! Dưới đây là 3 người có điểm số cao nhất:**")
    for i, (name, score) in enumerate(top_3):
        st.write(f"**{i + 1}. {name}** với số điểm: {score} điểm")
    # Fun message for the top participant
    if top_3:
        st.write(f"🏆 Sau 2 vòng thi căng thẳng, **{top_3[0][0]}** là người hiểu mẹ Lan nhất quả đất 🤯 Sốc ngang!")
    # Fun message for the lowest participant
    if lowest_3:
        st.write(f"😂 Ngoài ra thì có **{lowest_3[0][0]}** cần đi chơi với mẹ/bác/chị Lan để hiểu nhau hơn!")
    
    # Button to proceed to the memory section
    if st.button("Tiếp tục đến phần lời chúc"):
        st.session_state.show_memory_section = True


# Display total scores in the sidebar
def display_sidebar_scores():
    st.sidebar.subheader("Điểm hiện tại:")
    for child, score in st.session_state.scores.items():
        st.sidebar.markdown(f"- **{child}**: {score} điểm")

# Main function to run the app
def main():
    st.title("Chúc mừng sinh nhật mẹ Lan 23/09/2024")

    # Initialize scores in session state if not already done
    if 'scores' not in st.session_state:
        st.session_state.scores = {child: 0 for child in ["Mẹ ngoại", "Cậu Quang", "Mẹ Mai Anh", "Hà Linh", "Trung", "Nguyên", "Nghé"]}

    # Initialize current question, current photo index, and memory section toggle in session state if not already done
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'current_photo' not in st.session_state:
        st.session_state.current_photo = 0
    if 'show_memory_section' not in st.session_state:
        st.session_state.show_memory_section = False

    # Questions and answers data for Section 1
    questions = [
        "Yếu tố quan trọng nhất khiến mẹ/bác/chị Lan thấy một bộ phim hay?",
        "Khi ra khỏi nhà, mẹ/bác/chị Lan dễ quên đồ gì nhất?",
        "Mẹ/bác/chị Lan sẽ làm gì khi bực mình?",
        "Địa điểm du lịch mà mẹ/bác/chị Lan muốn đến tiếp theo?",
        "Điều gì mẹ Lan thấy mình làm rất giỏi nhưng ít người biết?"
    ]
    answers_by_child = [
        {"Mẹ ngoại": "Sample", "Cậu Quang": "Tiếng Anh dễ nghe", "Mẹ Mai Anh": "Hành động, diễn viên đẹp", "Hà Linh": "Diễn viên đẹp trai xinh gái", "Trung": "Sample", "Nguyên": "1F", "Nghé": "Sample"},
        {"Mẹ ngoại": "Sample", "Cậu Quang": "Não 😂", "Mẹ Mai Anh": "Chìa khóa, điện thoại", "Hà Linh": "Điện thoại", "Trung": "Sample", "Nguyên": "Sample", "Nghé": "Sample"},
        {"Mẹ ngoại": "Sample", "Cậu Quang": "Làm việc", "Mẹ Mai Anh": "Xả luôn!", "Hà Linh": "Cằn nhằn liên tục", "Trung": "Sample", "Nguyên": "Sample", "Nghé": "Sample"},
        {"Mẹ ngoại": "Sample", "Cậu Quang": "Machu Picchu", "Mẹ Mai Anh": "Mexico", "Hà Linh": "Châu Âu", "Trung": "Sample", "Nguyên": "Sample", "Nghé": "Sample"},
        {"Mẹ ngoại": "Sample", "Cậu Quang": "Sinh tố", "Mẹ Mai Anh": "Nấu ăn", "Hà Linh": "Ca hát", "Trung": "Sample", "Nguyên": "Sample", "Nghé": "Sample"}
    ]

    # Photo guessing data for Section 2
    photos = {
        "photo1.jpg": "Ảnh này được chụp ở đâu, vào năm nào?",
        "photo2.jpg": "Ảnh này được chụp ở đâu, vào năm nào?",
        "photo3.jpg": "Ảnh này được chụp ở đâu, vào năm nào?"
    }
    guesses_by_child = [
        {"Mẹ ngoại": "Guess 1A", "Cậu Quang": "Guess 1B", "Mẹ Mai Anh": "Guess 1C", "Hà Linh": "Guess 1D", "Trung": "Guess 1E", "Nguyên": "Guess 1F", "Nghé": "Guess 1G"},
        {"Mẹ ngoại": "Guess 2A", "Cậu Quang": "Guess 2B", "Mẹ Mai Anh": "Guess 2C", "Hà Linh": "Guess 2D", "Trung": "Guess 2E", "Nguyên": "Guess 2F", "Nghé": "Guess 2G"},
        {"Mẹ ngoại": "Guess 3A", "Cậu Quang": "Guess 3B", "Mẹ Mai Anh": "Guess 3C", "Hà Linh": "Guess 3D", "Trung": "Guess 3E", "Nguyên": "Guess 3F", "Nghé": "Guess 3G"}
    ]

    # Video URLs for Section 3
    children_videos = {
        "Mẹ ngoại": "https://youtu.be/tuQ5DIUFlHs?si=4dQZ9oC1V1faYFBu",
        "Cậu Quang": "https://youtu.be/tuQ5DIUFlHs?si=4dQZ9oC1V1faYFBu",
        "Mẹ Mai Anh": "https://youtu.be/tuQ5DIUFlHs?si=4dQZ9oC1V1faYFBu",
        "Hà Linh": "https://youtu.be/tuQ5DIUFlHs?si=4dQZ9oC1V1faYFBu",
        "Trung": "https://youtu.be/tuQ5DIUFlHs?si=4dQZ9oC1V1faYFBu",
        "Nguyên": "https://youtu.be/tuQ5DIUFlHs?si=4dQZ9oC1V1faYFBu",
        "Nghé": "https://youtu.be/tuQ5DIUFlHs?si=4dQZ9oC1V1faYFBu"
    }

    # Display MCQ section (question-by-question)
    mcq_section(questions, answers_by_child)

    # Once MCQ section is done, move to photo section
    if st.session_state.current_question == len(questions):
        photo_mcq_section(photos, guesses_by_child)

    # Once photo section is done, move to score conclusion section
    if st.session_state.current_photo == len(photos):
        if not st.session_state.show_memory_section:
            score_conclusion_section()
        else:
            memory_section(children_videos)

    # Display the updated scores in the sidebar
    display_sidebar_scores()

if __name__ == "__main__":
    main()
