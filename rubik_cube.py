# pip install ursina

from ursina import *
from ursina import EditorCamera
from ursina import invoke  # 수정: invoke 함수 import 추가 (2025-04-17 20:50:00)
import random

app = Ursina()

# 전역 변수 초기화
cube_size = 3
pieces = []
rotation_parent = None
animating = False
scramble_moves = []

# 카메라 설정
EditorCamera()
camera.fov = 40

# 큐브 생성 함수
def create_cube(n):
    global pieces
    # 기존 큐비 제거
    for p in pieces:
        destroy(p)
    pieces.clear()
    r = (n - 1) / 2
    # 외부 큐비만 생성
    for x in range(n):
        for y in range(n):
            for z in range(n):
                pos = Vec3(x - r, y - r, z - r)
                if abs(pos.x) == r or abs(pos.y) == r or abs(pos.z) == r:
                    parent_entity = Entity()
                    parent_entity.position = pos
                    pieces.append(parent_entity)
                    # 면마다 색상 부여
                    if pos.y == r: create_face(parent_entity, Vec3(0,1,0), color.white)
                    if pos.y == -r: create_face(parent_entity, Vec3(0,-1,0), color.yellow)
                    if pos.x == -r: create_face(parent_entity, Vec3(-1,0,0), color.green)
                    if pos.x == r: create_face(parent_entity, Vec3(1,0,0), color.blue)
                    if pos.z == r: create_face(parent_entity, Vec3(0,0,1), color.red)
                    if pos.z == -r: create_face(parent_entity, Vec3(0,0,-1), color.orange)

# 큐비 면 생성 함수
def create_face(parent_entity, direction, face_color):
    f = Entity(model='quad', color=face_color, parent=parent_entity)
    f.position = direction * 0.5
    f.rotation = Vec3(direction.z*90, direction.x*-90, 0)

# 위치 및 회전 반올림
def round_transform(e):
    e.position = Vec3(round(e.position.x,3), round(e.position.y,3), round(e.position.z,3))
    e.rotation = Vec3(round(e.rotation.x,3), round(e.rotation.y,3), round(e.rotation.z,3))

# 표기법 → 축, 레이어, 각도 변환
def face_to_axis(face):
    amount = 90
    if face.endswith('2'):
        amount = 180
        face = face[0]
    elif face.endswith("'"):
        amount = -90
        face = face[0]
    face = face[0]
    r = (cube_size - 1) / 2
    axis_map = {
        'U': ('y', r), 'D': ('y', -r),
        'L': ('x', -r), 'R': ('x', r),
        'F': ('z', r), 'B': ('z', -r),
    }
    axis, index = axis_map[face]
    return axis, index, amount

# 면 회전 함수
def rotate_face(face_move, record=True):
    global animating, rotation_parent
    if animating:
        return
    animating = True
    axis, index, amount = face_to_axis(face_move)
    # 해당 레이어 조각 수집
    group = [p for p in pieces if getattr(p.position, axis) == index]
    # 임시 부모로 그룹화
    rotation_parent = Entity()
    for p in group:
        p.parent = rotation_parent
    target = Vec3()
    setattr(target, axis, amount)
    # 애니메이션 및 콜백
    def finish():
        global animating
        for c in rotation_parent.children:
            c.parent = scene
            c.world_rotation += rotation_parent.rotation
            round_transform(c)
            c.position = c.world_position
        destroy(rotation_parent)
        if record:
            scramble_moves.append(face_move)
        animating = False
    rotation_parent.animate('rotation', rotation_parent.rotation + target, duration=0.15, curve=curve.linear)  # 수정: Entity.animate 메서드 사용 (2025-04-17 20:51:00)
    invoke(finish, delay=0.15)  # 수정: 애니메이션 완료 후 finish 호출 (2025-04-17 20:50:00)

# UI 요소 생성
size_input = InputField(text=str(cube_size), max_length=1, width=0.1)
set_btn = Button(text='Set', color=color.azure, scale=(.1,.05), on_click=lambda: apply_size())
scramble_btn = Button(text='Scramble', color=color.orange, scale=(.1,.05), on_click=lambda: start_scramble())
solve_btn = Button(text='Solve', color=color.lime, scale=(.1,.05), on_click=lambda: start_solve())
reset_btn = Button(text='Reset View', color=color.light_gray, scale=(.1,.05), on_click=lambda: reset_view())
panel = Entity(parent=camera.ui)
for btn in [size_input, set_btn, scramble_btn, solve_btn, reset_btn]:
    btn.parent = panel
size_input.x, size_input.y = -0.4, 0.4
set_btn.x, set_btn.y = -0.2, 0.4
scramble_btn.x, scramble_btn.y = 0.0, 0.4
solve_btn.x, solve_btn.y = 0.2, 0.4
reset_btn.x, reset_btn.y = 0.4, 0.4

# UI 콜백 함수들
def apply_size():
    global cube_size, scramble_moves
    try:
        n = int(size_input.text)
        if not 1 <= n <= 9:
            raise ValueError
        cube_size = n
        scramble_moves.clear()
        create_cube(cube_size)
    except:
        print("입력 오류: 1~9 사이의 정수를 입력하세요.")

def start_scramble():
    if animating:
        return
    moves = ['U','U\'','U2','D','D\'','D2','L','L\'','L2','R','R\'','R2','F','F\'','F2','B','B\'','B2']
    count = random.randint(20,30)
    for m in random.choices(moves, k=count):
        rotate_face(m, record=True)

def inverse_move(m):
    if m.endswith('2'):
        return m
    if m.endswith("'"):
        return m[0]
    return m + "'"

def start_solve():
    if animating:
        return
    for m in reversed(scramble_moves):
        rotate_face(inverse_move(m), record=False)
    scramble_moves.clear()

def reset_view():
    camera.target.position = Vec3(0,0,0)
    camera.rotation = Vec3(30,45,0)

# 초기화 및 실행
create_cube(cube_size)
app.run()
