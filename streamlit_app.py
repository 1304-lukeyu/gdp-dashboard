# streamlit_app.py

import streamlit as st

# --- 1. 앱 기본 설정 ---
st.set_page_config(
    page_title="Streamlit 틱택토 게임",
    page_icon="🕹️"
)

# --- 2. 게임 상태 초기화 함수 ---
def initialize_game():
    """
    st.session_state를 사용하여 게임에 필요한 모든 변수를 초기화합니다.
    - board: 3x3 게임 보드 (9개의 빈 문자열로 구성된 리스트)
    - turn: 현재 플레이어 ('X' 또는 'O')
    - winner: 게임 승자 (None, 'X', 'O', 'Draw')
    - game_over: 게임 종료 여부 (True/False)
    """
    if 'board' not in st.session_state:
        st.session_state.board = [''] * 9
        st.session_state.turn = 'X'
        st.session_state.winner = None
        st.session_state.game_over = False

# --- 3. 승리 조건 확인 함수 ---
def check_winner(board):
    """
    현재 보드 상태를 기반으로 승자를 확인합니다.
    - 가로, 세로, 대각선 3칸이 같은 플레이어의 마크로 채워졌는지 확인합니다.
    - 승자가 있으면 해당 플레이어('X' 또는 'O')를 반환하고, 없으면 None을 반환합니다.
    """
    # 승리 가능한 모든 경우의 수 (인덱스 기준)
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 가로
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 세로
        [0, 4, 8], [2, 4, 6]             # 대각선
    ]
    for combo in win_conditions:
        # 3개의 위치에 있는 값이 모두 동일하고, 비어있지 않은 경우
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != '':
            return board[combo[0]]
    return None

# --- 4. 앱 UI 및 로직 구성 ---

# 앱 제목 표시
st.title("🕹️ 틱택토 (Tic-Tac-Toe)")
st.write("---")

# 게임 상태 초기화 함수 호출
initialize_game()

# 게임 보드판과 버튼을 그리기 위한 스타일 (선택 사항)
# 버튼을 정사각형으로 만들고 텍스트를 크게하여 게임 보드처럼 보이게 합니다.
st.markdown("""
<style>
    /* stButton 클래스를 가진 요소 내부의 button 태그에 스타일 적용 */
    .stButton>button {
        width: 100px;
        height: 100px;
        font-size: 2.5em;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# --- 게임 상태에 따른 메시지 표시 ---
if st.session_state.game_over:
    if st.session_state.winner == "Draw":
        st.info("🤝 무승부입니다! 다시 시작하세요.")
    else:
        # 이모지와 함께 승리 메시지를 크게 표시
        st.success(f"🎉 **{st.session_state.winner}** 플레이어 승리! 🎉")
else:
    # 현재 누구의 턴인지 안내
    st.write(f"🔵 **{st.session_state.turn}** 플레이어 차례입니다.")


# --- 게임 보드판 생성 ---
# st.columns를 사용하여 3x3 격자를 만듭니다.
cols = st.columns(3)
for i in range(9):
    with cols[i % 3]:
        # 각 칸에 버튼을 생성합니다. 버튼의 레이블은 보드 상태('X', 'O', 또는 공백)를 표시합니다.
        # key를 고유하게 설정하여 각 버튼을 구분합니다.
        if st.button(st.session_state.board[i] if st.session_state.board[i] else " ", key=f'cell-{i}'):
            # 버튼 클릭 시 실행될 로직
            # 해당 칸이 비어있고 게임이 끝나지 않았을 경우에만 진행
            if st.session_state.board[i] == '' and not st.session_state.game_over:
                # 현재 플레이어의 마크를 보드에 표시
                st.session_state.board[i] = st.session_state.turn
                
                # 승자 확인
                winner = check_winner(st.session_state.board)
                if winner:
                    st.session_state.winner = winner
                    st.session_state.game_over = True
                # 보드가 꽉 찼는지 (무승부인지) 확인
                elif '' not in st.session_state.board:
                    st.session_state.winner = "Draw"
                    st.session_state.game_over = True
                # 게임이 계속되면 턴을 넘김
                else:
                    st.session_state.turn = 'O' if st.session_state.turn == 'X' else 'X'
                
                # 버튼 클릭 후 화면을 즉시 새로고침하여 변경사항을 반영
                st.rerun()

st.write("---")

# --- 새 게임 시작 버튼 ---
if st.button("🔄️ 새 게임 시작하기"):
    # session_state의 모든 값을 삭제하여 게임을 초기 상태로 리셋
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    # 화면 새로고침
    st.rerun()