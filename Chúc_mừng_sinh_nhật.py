import streamlit as st
from streamlit_timeline import timeline

# Section 1: MCQs Questions about Self
def mcq_section(questions, answers_by_child):
    st.subheader("Vòng 1: Ai hiểu mẹ Lan nhất?!")
    
    selected_answers = {}
    # Display all questions at once
    for idx, question in enumerate(questions):
        st.write(f"Câu {idx + 1}: {question}")
        
        # Display the answer options from each contestant
        options = [f"{name}: {answer}" for name, answer in answers_by_child[idx].items()]
        options.append("Không có câu nào đúng cả")  # Add "None of the above" option
        
        selected_answers[idx] = st.multiselect(f"Mẹ hãy chọn câu trả lời đúng nhất cho Câu {idx + 1}:", options, key=f"q_{idx}")
    
    return selected_answers

# Section 2: MCQs for Photos (Guessing event/year)
def photo_mcq_section(photos, guesses_by_child):
    st.subheader("Vòng 2: Nhìn hình đoán địa điểm")

    selected_photo_answers = {}
    # Display all photos at once
    for idx, (photo_url, question) in enumerate(photos.items()):
        st.write(f"Ảnh {idx + 1}: {question}")
        st.image(photo_url, use_column_width=True)
        
        # Display the guessing options
        options = [f"{name}: {guess}" for name, guess in guesses_by_child[idx].items()]
        options.append("Không có câu nào đúng cả")  # Add "None of the above" option
        
        selected_photo_answers[idx] = st.multiselect(f"Mẹ hãy chọn câu trả lời đúng nhất cho Ảnh {idx + 1}:", options, key=f"photo_{idx}")
    
    return selected_photo_answers

# Section 3: Sharing Videos and Memories (No scoring here)
def memory_section(children_videos):
    st.subheader("Vòng 3: Lời chúc từ cả nhà")

    # Tabs for each child
    tabs = st.tabs([f"{child}" for child in children_videos.keys()])
    
    for i, (child, video_url) in enumerate(children_videos.items()):
        with tabs[i]:
            st.write(f"Lời chúc của {child}")
            st.video(video_url)
            st.write(f"Lời chúc của {child}!")

# Section to display the final scores and show top 3 participants
def score_conclusion_section():
    st.subheader("Kết quả vòng thi!")
    
    # Sort the scores in descending order to get top 3 and lowest 3
    sorted_scores = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
    
    # Top 3 participants
    top = sorted_scores[:3]
    for i in range(2, len(sorted_scores)-1):
        if sorted_scores[i][1]==sorted_scores[i+1][1]:
            top = sorted_scores[:i+1]
        else:
            break
    
    # Lowest 3 participants
    lowest = sorted(sorted_scores, key=lambda x: x[1])[:3]
    for i in range(2, len(sorted_scores)-1):
        if sorted_scores[i][1]==sorted_scores[i+1][1]:
            lowest = sorted(sorted_scores, key=lambda x: x[1])[:i+1]
        else:
            break

    # Display the top 3 participants
    st.write("🎉 **Cảm ơn cả nhà đã tham gia trò chơi! Dưới đây là những người có điểm số cao nhất:**")
    prev_score=0
    i=-1
    for (name, score) in enumerate(top):
        i += 1
        if prev_score==score:
            i -= 1
        st.write(f"**{i}. {name}** với số điểm: {score} điểm")
        prev_score = score
    
    # Fun message for the top participant
    if top:
        if top[0][1]!=top[1][1]:
            st.write(f"🏆 Sau 2 vòng thi căng thẳng, **{top[0][0]}** là người hiểu mẹ Lan nhất quả đất 🤯 Sốc ngang!")
        else:
            string = top[0][0]
            for i in range(len(top)-1):
                if top[i][1] == top[i+1][1]:
                    string = string + " và " + top[i+1][0]
                else:
                    st.write(f"🏆 Sau 2 vòng thi căng thẳng, **{string}** là người hiểu mẹ Lan nhất quả đất 🤯 Sốc ngang!")
                    break
    
    # Fun message for the lowest participant
    if lowest:
        if lowest[0][1]!=lowest[1][1]:
            st.write(f"😂 Ngoài ra thì có **{lowest[0][0]}** cần đi chơi với mẹ/bác/chị Lan để hiểu nhau hơn!")
        else:
            string = lowest[0][0]
            for i in range(len(lowest)-1):
                if lowest[i][1] == lowest[i+1][1]:
                    string = string + " và " + lowest[i+1][0]
                else:
                    st.write(f"😂 Ngoài ra thì có **{string}** cần đi chơi với mẹ/bác/chị Lan để hiểu nhau hơn!")
                    break

# Section to display the timeline (this will always show when the memory section is shown)
def display_timeline():
    with open('timeline.json', "r") as f:
        data = f.read()
    
    # Render timeline
    timeline(data, height=800)


# Main function to run the app
def main():
    st.title("Chúc mừng sinh nhật mẹ 🎉💃")

    # Initialize scores and state flags in session state if not already done
    if 'scores' not in st.session_state:
        st.session_state.scores = {child: 0 for child in ["Mẹ ngoại", "Cậu Quang", "Mẹ Mai Anh", "Hà Linh", "Trung", "Nguyên", "Nghé"]}
    
    if 'show_memory_section' not in st.session_state:
        st.session_state.show_memory_section = False
    
    if 'scoring_done' not in st.session_state:
        st.session_state.scoring_done = False

    # Questions and answers data for Section 1
    questions = [
        "Yếu tố quan trọng nhất khiến mẹ/bác/chị Lan thấy **một bộ phim hay**?",
        "Khi ra khỏi nhà, mẹ/bác/chị Lan dễ **quên đồ gì nhất**?",
        "Mẹ/bác/chị Lan sẽ **làm gì khi bực mình**?",
        "Địa điểm du lịch mà mẹ/bác/chị Lan **muốn đến tiếp theo**?",
        "Điều gì mẹ Lan thấy mình làm **rất giỏi** nhưng **ít người biết**?"
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
        "photo3.jpg": "Ảnh này được chụp ở đâu, vào năm nào?",
        "photo4.jpg": "Ảnh này được chụp ở đâu, vào năm nào?"
    }
    guesses_by_child = [
        {"Mẹ ngoại": "Guess 1A", "Cậu Quang": "Guess 1B", "Mẹ Mai Anh": "Guess 1C", "Hà Linh": "Guess 1D", "Trung": "Guess 1E", "Nguyên": "Guess 1F", "Nghé": "Guess 1G"},
        {"Mẹ ngoại": "Guess 2A", "Cậu Quang": "Guess 2B", "Mẹ Mai Anh": "Guess 2C", "Hà Linh": "Guess 2D", "Trung": "Guess 2E", "Nguyên": "Guess 2F", "Nghé": "Guess 2G"},
        {"Mẹ ngoại": "Guess 3A", "Cậu Quang": "Guess 3B", "Mẹ Mai Anh": "Guess 3C", "Hà Linh": "Guess 3D", "Trung": "Guess 3E", "Nguyên": "Guess 3F", "Nghé": "Guess 3G"},
        {"Mẹ ngoại": "Guess 4A", "Cậu Quang": "Guess 4B", "Mẹ Mai Anh": "Guess 4C", "Hà Linh": "Guess 4D", "Trung": "Guess 4E", "Nguyên": "Guess 4F", "Nghé": "Guess 4G"}
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

    # Display MCQ section
    selected_mcq_answers = mcq_section(questions, answers_by_child)
    st.divider()

    # Display photo guessing section
    selected_photo_answers = photo_mcq_section(photos, guesses_by_child)

    # Button to calculate scores and display final results
    if st.button("Tính điểm và hiện kết quả") and not st.session_state.scoring_done:
        # Calculate scores based on selected options (MCQ + Photos)
        for idx, selected in selected_mcq_answers.items():
            for option in selected:
                child_name = option.split(":")[0]
                if child_name in st.session_state.scores and "Không có câu nào đúng cả" not in option:
                    st.session_state.scores[child_name] += 1
        
        for idx, selected in selected_photo_answers.items():
            for option in selected:
                child_name = option.split(":")[0]
                if child_name in st.session_state.scores and "Không có câu nào đúng cả" not in option:
                    st.session_state.scores[child_name] += 1
        
        st.session_state.scoring_done = True  # Mark scoring as done to avoid recalculating

    # Always show scores if scoring is done
    if st.session_state.scoring_done:
        score_conclusion_section()

    # Show button to reveal the memory videos after the scores are displayed
    if st.session_state.scoring_done and st.button("Tiếp tục đến phần lời chúc"):
        st.session_state.show_memory_section = True

    # Show memory videos only after clicking the button
    if st.session_state.show_memory_section:
        memory_section(children_videos)
        display_timeline()

if __name__ == "__main__":
    main()
