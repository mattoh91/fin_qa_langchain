css = """
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
.footer {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  background-color: white;
  color: black;
  text-align: center;
}
.reference-font {
  font-size: 10px;
  opacity: 0.5;
}

"""

bot_template = """
<div class="chat-message bot">
    <div class="avatar">
        <img src="data:image/png;base64,{{IMG}}">
    </div>
    <div class="message">{{MSG}}</div>
</div>
"""

user_template = """
<div class="chat-message user">
    <div class="avatar">
        <img src="data:image/png;base64,{{IMG}}">
    </div>
    <div class="message">{{MSG}}</div>
</div>
"""

reference_template = """
<div class="footer">
    <p class="reference-font">Icons by freepik and stasy</p>
</div>
"""
