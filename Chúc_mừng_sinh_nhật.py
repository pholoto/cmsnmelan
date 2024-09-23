import streamlit as st
from streamlit_timeline import timeline
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

# # Prepare the word data
# def get_word_cloud_data():
#     # Words collected from different individuals
#     word_data = """
#     Lạc quan,
#     Dễ quên,
#     Hào phóng,
#     Tự tin,
#     Không sợ bàn tán,
#     Không sợ thử,
#     Tỉnh táo,
#     Kiên nhẫn,
#     Tích cực,
#     Vui vẻ, 
#     Tích cực, 
#     Dễ thương,
#     Vui vẻ, 
#     Bình tĩnh, 
#     Nhẹ nhàng,
#     Lạc quan, 
#     Mạnh mẽ, 
#     Tích cực,
#     Năng lượng, 
#     Tích cực, 
#     Lạc quan, 
#     Trẻ trung
#     """
#     return word_data

# # Function to clean and count word frequencies
# def process_word_data(word_data):
#     # Clean up the data: remove commas and strip spaces
#     words = [word.strip() for word in word_data.replace(",", "").splitlines()]
    
#     # Count the frequency of each word/phrase
#     word_freq = Counter(words)
    
#     return word_freq

# # Function to generate and display the word cloud
# def display_word_cloud():
    
#     # Get the data and process it into a frequency dictionary
#     word_data = get_word_cloud_data()
#     word_freq = process_word_data(word_data)
    
#     # Generate the word cloud from the frequency dictionary
#     wordcloud = WordCloud(width=800, height=400, background_color="white", colormap='tab20b', prefer_horizontal=1.0).generate_from_frequencies(word_freq)
    
#     # Display the word cloud using matplotlib
#     fig, ax = plt.subplots(figsize=(10, 5))
#     ax.imshow(wordcloud.recolor(random_state=3), interpolation='bilinear')
#     ax.axis("off")  # No axes for the word cloud

#     # Show the word cloud using Streamlit
#     st.pyplot(fig)


# Section 1: MCQs Questions about Self
def mcq_section(questions, answers_by_child):
    st.subheader("Vòng 1: Ai hiểu mẹ Lan nhất?!")
    
    selected_answers = {}
    # Display all questions at once
    for idx, question in enumerate(questions):
        st.divider()
        st.write(f"Câu {idx + 1}: {question}")
        
        # Display the answer options from each contestant
        options = [f"{name}: {answer}" for name, answer in answers_by_child[idx].items()]
        
        selected_answers[idx] = st.multiselect(f"Mẹ hãy chọn câu trả lời đúng nhất cho Câu {idx + 1}:", options, key=f"q_{idx}")
    
    return selected_answers

# Section 2: MCQs for Photos (Guessing event/year)
def photo_mcq_section(photos, guesses_by_child):
    st.subheader("Vòng 2: Nhìn hình đoán địa điểm")

    selected_photo_answers = {}
    # Display all photos at once
    for idx, (photo_url, question) in enumerate(photos.items()):
        st.divider()
        st.write(f"Ảnh {idx + 1}: {question}")
        st.image(photo_url, width=400)
        
        # Display the guessing options
        options = [f"{name}: {guess}" for name, guess in guesses_by_child[idx].items()]
        
        selected_photo_answers[idx] = st.multiselect(f"Mẹ hãy chọn câu trả lời đúng nhất cho Ảnh {idx + 1}:", options, key=f"photo_{idx}")
    
    return selected_photo_answers

# Section 3: Sharing Videos and Memories (No scoring here)
def memory_section(children_videos):
    st.subheader("Vòng 3: Lời chúc từ cả nhà")

    # Example of different messages for each child
    custom_messages = {
        "Mẹ ngoại": "\"Chúc con gái **mạnh khỏe, vui vẻ, dành nhiều thời gian cho bản thân** nhé!\"",
        "Cậu Quang và Nghé": "\"Nghé chúc bác Mai Lan **sự nghiệp trên đỉnh thành công**, nhưng vẫn có thời gian **nghỉ ngơi và tận hưởng** thế giới... Ngoài ra xinh đẹp hơn và đạt được chức cao hơn! Em Quang chúc chị trở thành **ca sĩ của năm, múa yoga dẻo hơn**. Happy birthday 🎉🎉🎉\"",
        "Mẹ Mai Anh": "\"Chị Mai Anh chúc em luôn **trẻ trung, tràn đầy năng lượng và tiếp tục lan tỏa sự tích cực tới mọi người, luôn may mắn, và thật nhiều sức khỏe**.\"",
        "Hà Linh": "\"Con chúc mẹ Lan **nhiều thời gian để trau dồi khả năng ca hát nghệ thuật, học thêm các kĩ năng mới, và thật nhiều sức khỏe, niềm vui, luôn cảm thấy hạnh phúc**.\"",
        "Trung": "\"Con chúc mẹ Lan **nhiều sinh viên đạt kết quả tốt và tuyển được nhiều sinh viên, đồng thời vẫn có nhiều thời gian rảnh để làm những điều mình thích**.\"",
        "Nguyên": "\"Con chúc mẹ Lan **luôn luôn mạnh khỏe, ít căng thẳng vì công việc và ít phải lo lắng cho bọn con** hơn. Thay vào đó mẹ có thể có thêm **nhiều thời gian để đi du lịch, khám phá các nơi trên thế giới** ạ.\""
    }

    # Tabs for each child
    tabs = st.tabs([f"{child}" for child in children_videos.keys()])
    
    # Iterate through children and display content in respective tabs
    for i, (child, video_url) in enumerate(children_videos.items()):
        with tabs[i]:
            # Display custom message for each child
            custom_message = custom_messages.get(child, f"Lời chúc của {child} nhân ngày sinh nhật mẹ Lan!")
            st.write(custom_message)
            st.video(video_url)

# Section to display the final scores and show top 3 participants
def score_conclusion_section():
    st.subheader("Kết quả vòng thi!")
    
    # Sort the scores in descending order to get top 3 and lowest 3
    sorted_scores = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
    
    # Top 3 participants
    top = sorted_scores[:3]
    for i in range(2, len(sorted_scores)-1):
        if sorted_scores[i][1]==sorted_scores[i+1][1]:
            top = sorted_scores[:i+2]
        else:
            break
    
    # Lowest 3 participants
    lowest = sorted(sorted_scores, key=lambda x: x[1])[:3]
    for i in range(2, len(sorted_scores)-1):
        if sorted_scores[i][1]==sorted_scores[i+1][1]:
            lowest = sorted(sorted_scores, key=lambda x: x[1])[:i+2]
        else:
            break

    # Display the top 3 participants
    st.write("🎉 **Cảm ơn cả nhà đã tham gia trò chơi! Dưới đây là kết quả chung cuộc:**")
    sorted_scores = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
    prev_score = -1
    i = 1
    for _, (name, score) in enumerate(sorted_scores):
        if prev_score==score:
            i -= 1
        st.write(f"**{i}. {name}** với số điểm: {score} điểm")
        i += 1
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
            st.write(f"😂 Ngoài ra thì có **{lowest[0][0]}** cần đi chơi với mẹ Lan để hiểu nhau hơn!")
        else:
            string = lowest[0][0]
            for i in range(len(lowest)-1):
                if lowest[i][1] == lowest[i+1][1]:
                    string = string + " và " + lowest[i+1][0]
                else:
                    st.write(f"😂 Ngoài ra thì có **{string}** cần đi chơi với mẹ Lan để hiểu nhau hơn!")
                    break

# Section to display the timeline (this will always show when the memory section is shown)
def display_timeline():
    with open('timeline.json', "r") as f:
        data = f.read()
    
    # Render timeline
    timeline(data, height=800)


# Main function to run the app
def main():
    st.title("Chúc mừng sinh nhật 🎉💃")

    st.write("Chúc mừng sinh nhật nhà giáo nhân dân kiêm cựu banker kiêm ca sĩ nổi danh Lê Mai Lan! Đây là một trang web nho nhỏ được tạo ra để gửi gắm tình iu của cả nhà tới mẹ Lan, gồm nhiều phần thú dị như những trò chơi hấp dẫn, các lời chúc có cánh, dòng thời gian đầy hoài niệm...")
    st.write("Để bắt đầu, hãy cùng điểm lại dòng thời gian từ tháng 9/2023 tới tháng 9/2024, xem một năm qua đã có những sự kiện, buổi ăn chơi lớn nào trong gia đình mà có sự góp mặt của mẹ Lan nhé!")
    display_timeline()

    st.write("Tiếp theo đây là những \"từ khóa\" cả nhà dành cho mẹ Lan khi được hỏi: Ba điều thấy ấn tượng nhất về mẹ Lan. Có thể thấy sự **tích cực, vui vẻ, lạc quan** được xuất hiện với tần suất rất cao, dường như là một đặc điểm signature của mẹ Lan! Ngoài ra, cũng toàn là những lời có cánh như **dễ thương, trẻ trung** quá chi là phù hợp 😗")
    st.image("wordcloud0.png", width=700)
    st.write("Tiếp sau đây, hãy cùng đến với trò chơi nho nhỏ: \"Ai là người hiểu mẹ Lan nhất?!\" và \"Nhìn hình đoán địa điểm\". Mẹ có thể lựa chọn nhiều hơn một đáp án đúng, hoặc không chọn đáp án nào cả nếu không có đáp án nào đúng.")
    
    # Initialize scores and state flags in session state if not already done
    if 'scores' not in st.session_state:
        st.session_state.scores = {child: 0 for child in ["Mẹ ngoại", "Cậu Quang", "Mẹ Mai Anh", "Hà Linh", "Trung", "Nguyên", "Nghé"]}
    
    if 'show_memory_section' not in st.session_state:
        st.session_state.show_memory_section = False
    
    if 'scoring_done' not in st.session_state:
        st.session_state.scoring_done = False

    # Questions and answers data for Section 1
    questions = [
        "Yếu tố quan trọng nhất khiến mẹ Lan thấy **một bộ phim hay**?",
        "Khi ra khỏi nhà, mẹ Lan dễ **quên đồ gì nhất**?",
        "Mẹ Lan sẽ **làm gì khi bực mình**?",
        "Địa điểm du lịch mà mẹ Lan **muốn đến tiếp theo**?",
        "Điều gì mẹ Lan thấy mình làm **rất giỏi** nhưng **ít người biết**?"
    ]
    answers_by_child = [
        {"Cậu Quang": "Tiếng Anh dễ nghe", "Mẹ Mai Anh": "Hành động, diễn viên đẹp", "Hà Linh": "Diễn viên đẹp trai xinh gái", "Trung": "Các trang phê bình phim bảo nó hay", "Nguyên": "Diễn viên giọng hay (accent Anh/Pháp hoặc hát hay)", "Nghé": "Phim dễ hiểu, diễn viên ưa nhìn"},
        {"Mẹ ngoại": "Tắt đèn💡", "Cậu Quang": "Não 😂", "Mẹ Mai Anh": "Chìa khóa 🔑 điện thoại 📱", "Hà Linh": "Điện thoại 📱", "Trung": "Tiền 💸", "Nguyên": "Túi xách đựng tiền 🛍️ và/hoặc điện thoại 📱", "Nghé": "Túi xách 🛍️"},
        {"Mẹ ngoại": "Không thấy Mai Lan bực bao giờ", "Cậu Quang": "Làm việc", "Mẹ Mai Anh": "Xả luôn!", "Hà Linh": "Cằn nhằn liên tục", "Trung": "Hét", "Nguyên": "Cứ kệ đấy 15 phút sau tự hết bực", "Nghé": "Chưa thấy bác Lan bực bao giờ"},
        {"Mẹ ngoại": "Nha Trang", "Cậu Quang": "Machu Picchu", "Mẹ Mai Anh": "Mexico", "Hà Linh": "Châu Âu", "Trung": "Châu Phi (các nơi thiên nhiên hoang dã)", "Nguyên": "Nam Mỹ (văn hóa Aztec các thứ)", "Nghé": "Châu Âu"},
        {"Mẹ ngoại": "Đối ngoại 👩‍💼", "Cậu Quang": "Sinh tố 🍹", "Mẹ Mai Anh": "Nấu ăn 🍝", "Hà Linh": "Ca hát 🎤", "Trung": "Chơi Golf 🏌️‍♂️", "Nguyên": "Dancing 💃", "Nghé": "Hát Karaoke 🎤"}
    ]

    # Photo guessing data for Section 2
    photos = {
        "photo1.jpg": "Ảnh này được chụp ở đâu, vào năm nào?",
        "photo2.jpg": "Ảnh này được chụp ở đâu, vào năm nào?",
        "photo3.jpg": "Ảnh này được chụp ở đâu, vào năm nào?",
        "photo4.jpg": "Ảnh này được chụp ở đâu, vào năm nào?"
    }
    guesses_by_child = [
        {"Cậu Quang": "Angkor Wat, 2014", "Mẹ Mai Anh": "Angkor Wat", "Hà Linh": "Angkor Wat, 2010", "Trung": "Angkor Thom, 2015", "Nguyên": "Đền nào đấy ở VN, 2018"},
        {"Cậu Quang": "Đức, 1995", "Mẹ Mai Anh": "Đức", "Hà Linh": "Đức, 1998", "Trung": "Đức, 1993", "Nguyên": "Đức, 1996"},
        {"Mẹ ngoại": "2023", "Cậu Quang": "Nha Trang, 2015", "Mẹ Mai Anh": "Khi vừa đổi kiểu tóc thảm họa", "Hà Linh": "Khởi công VinUni, 2019", "Trung": "VinUni động thổ, 2018", "Nguyên": "VinUni khởi công, 2019"},
        {"Cậu Quang": "Hà Nội, 2005", "Mẹ Mai Anh": "Khi mới đi làm sau khi sinh Trung Nguyên", "Hà Linh": "Vinschool, 2014", "Trung": "Vinschool, 2014", "Nguyên": "Vinschool, 2015"}
    ]

    # Video URLs for Section 3
    children_videos = {
        "Mẹ ngoại": "https://www.youtube.com/watch?v=ZabSEAC7cxw",
        "Cậu Quang và Nghé": "https://youtu.be/2WEjnqvQ-MI?si=xFL8fQsqv-2MM88C",
        "Mẹ Mai Anh": "https://youtu.be/cPafFtF4-ew?si=Hc94nrj2miYEEuu6",
        "Hà Linh": "https://youtu.be/tuQ5DIUFlHs?si=4dQZ9oC1V1faYFBu",
        "Trung": "https://youtu.be/2naapkQpU4A",
        "Nguyên": "https://www.youtube.com/watch?v=LSDAqii26P4"
    }

    # Display MCQ section
    selected_mcq_answers = mcq_section(questions, answers_by_child)
    st.divider()

    # Display photo guessing section
    selected_photo_answers = photo_mcq_section(photos, guesses_by_child)

    # Button to calculate scores and display final results
    if st.button("Tính điểm và hiện kết quả") and not st.session_state.scoring_done:
        # Calculate scores based on selected options (MCQ + Photos)
        
        # Section 1: MCQ questions scoring
        for idx, selected in selected_mcq_answers.items():
            if not selected:  # If no options were selected, skip scoring
                continue
            for option in selected:
                child_name = option.split(":")[0]
                if child_name in st.session_state.scores:
                    st.session_state.scores[child_name] += 1

        # Section 2: Photo MCQ questions scoring
        for idx, selected in selected_photo_answers.items():
            if not selected:  # If no options were selected, skip scoring
                continue
            for option in selected:
                child_name = option.split(":")[0]
                if child_name in st.session_state.scores:
                    st.session_state.scores[child_name] += 1

        st.session_state.scoring_done = True  # Mark scoring as done to avoid recalculating


    # Display the scores even after clicking to view the memory section
    if st.session_state.scoring_done:
        score_conclusion_section()  # Always display the scores if scoring is done
    
    # Show button to reveal the memory videos after the scores are displayed
    if st.session_state.scoring_done and st.button("Tiếp tục đến phần lời chúc"):
        st.session_state.show_memory_section = True

    # Show memory videos only after clicking the button
    if st.session_state.show_memory_section:
        memory_section(children_videos)
        st.divider()
        st.write("Chúc mừng sinh nhật mẹ Lan!!! 🎉💃🎊🎂 Hãy tự thưởng một chầu karaoke và 2 ly vang trắng nhá ạ 🎤🍷")
        st.image("photo0.png", use_column_width = True)

if __name__ == "__main__":
    main()
