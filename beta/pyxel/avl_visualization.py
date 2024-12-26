import pygame
import time

from pygame.math import Vector2

# Cấu hình Pygame
pygame.init()

#thay đổi kich thước màn hình
WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AVL Tree Visualization")
font = pygame.font.SysFont("Times New Roman", 20)
clock = pygame.time.Clock()
delta_time = 0

# Màu sắc  
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 150, 255)
GREEN = (100, 255, 100)
RED = (255, 100, 100)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)

# Hệ thống play animation
animation_play_1 = set()
animation_play_2 = set()
animation_play_3 = set()

animation_queue = []
animation_select = None

def run_animation():
    global animation_play_1
    global animation_play_2
    global animation_play_3

    global animation_queue
    global animation_select

    animation_run = animation_play_3 if len(animation_play_3) != 0 else None
    if len(animation_play_2) != 0:
        animation_run = animation_play_2
    if len(animation_play_3) != 0:
        animation_run = animation_play_3

    if animation_run is not None:
        trash = set()

        for animation in animation_run:
            try:
                next(animation)
            except:
                trash.add(animation)
        
        if len(trash) != 0:
            animation_run -= trash

    # Play animation queue
    if len(animation_queue) != 0 and animation_select is None:
        animation_select = animation_queue.pop(0)

    if animation_select is not None:
        try:
            next(animation_select)
        except:
            animation_select = None

def animation_repeat(seconds, funtor):
    global delta_time

    counter = 0
    while counter < seconds:
        counter += delta_time
        funtor()
        yield None

def animation_pause(seconds):
    global delta_time

    counter = 0
    while counter < seconds:
        counter += delta_time
        yield None

tree = None

# Node cho AVL Tree
class Node:
    def __init__(self, key, position):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.height = 1
        self.position = position
    
    def update_height(self):
        left_height = self.left.height if self.left is not None else 0
        right_height = self.right.height if self.right is not None else 0
        self.height = 1 + max(left_height, right_height)

    def get_balance(self):
        left_height = self.left.height if self.left is not None else 0
        right_height = self.right.height if self.right is not None else 0
        return left_height - right_height
    
    def rotate_right(self):
        parent = self.left

        self.left = parent.right
        if self.left is not None:
            self.left.parent = self

        parent.right = self
        parent.parent = self.parent
        self.parent = parent

        self.update_height()
        parent.update_height()

        p_parent = parent.parent
        if p_parent is not None:
            if p_parent.left is self:
                p_parent.left = parent
            else:
                p_parent.right = parent
        return parent
    
    def rotate_left(self):
        parent = self.right

        self.right = parent.left
        if self.right is not None:
            self.right.parent = self

        parent.left = self
        parent.parent = self.parent
        self.parent = parent

        self.update_height()
        parent.update_height()

        p_parent = parent.parent
        if p_parent is not None:
            if p_parent.left is self:
                p_parent.left = parent
            else:
                p_parent.right = parent

        return parent
    
    def _make_nodes(self, lst):
        lst.append(self)

        if self.left is not None:
            self.left._make_nodes(lst)
        if self.right is not None:
            self.right._make_nodes(lst)

    def set_position(self, root, position, dx):
        self.position = position
        if self.key < root.key:
            self.set_position(root.left, position + Vector2(-dx, 100), dx // 2)
        else:
            self.set_position(root.right, position + Vector2(dx, 100), dx // 2)

    def get_position(self, position, dx):
        if self.parent is None:
            return position

        # False : left
        # True  : right
        list_bin = []
        parent = self.parent
        node = self

        while parent is not None:
            list_bin.insert(0, parent.left is not node) # sẽ sai nếu dùng "parent.right is node"
            node = parent
            parent = node.parent
        
        for _bin in list_bin:
            if _bin:
                position += Vector2(dx, 100)
            else:
                position += Vector2(-dx, 100)
            dx //= 2
        return position

    def animation_move(self):
        global delta_time

        speed = 600
        position = self.get_position(Vector2(WIDTH // 2, 50), 350)
        vec = (position - self.position).normalize()

        while True:
            step = vec * speed * delta_time
            if (position - self.position).magnitude() < step.magnitude():
                self.position = position
                break

            self.position += step
            yield None

def draw_root(root):
    if root is None:
        return

    balance = root.get_balance()

    pygame.draw.circle(screen, BLUE, root.position, 20)
    text = font.render(str(root.key), True, WHITE)
    screen.blit(text, root.position - Vector2(text.get_width() // 2, text.get_height() // 2))

    balance_text = font.render(f"{root.height}", True, BLACK)
    screen.blit(balance_text, root.position + Vector2(-balance_text.get_width() // 2, 25))

    if root.left:
            pygame.draw.line(screen, BLACK, root.position, root.left.position, 2)
            draw_root(root.left)
            
    if root.right:
            pygame.draw.line(screen, BLACK, root.position, root.right.position, 2)
            draw_root(root.right)

def animation_move(nodes, positions):
    speed = 600
    vecs = []
    for i in range(len(nodes)):
        node, position = nodes[i], positions[i]
        vecs.append((position - node.position).normalize())
    flags = [False] * len(nodes)

    while all(flags) is False:
        for i in range(len(nodes)):
            if flags[i]:
                continue

            node, position = nodes[i], positions[i]
            step = vecs[i] * speed * delta_time
            if (position - node.position).magnitude() < step.magnitude():
                node.position = position
                flags[i] = True
            else:
                node.position += step
            yield None

class AVL:
    def __init__(self):
        self.root = None
    
    def search(self, key):
        root = self.root

        while root is not None:
            if root.key == key:
                return root
            elif root.key > key:
                root = root.left
            else:
                root = root.right
        
        return None

    def insert(self, key):
        # Thông báo : nhập giá trị đã tồn tại
        if self.search(key):
            self.show_duplicate_message()
            return

        if self.root is None:
            self.root = Node(key, Vector2(WIDTH // 2, 50))
            return
        
        # Play animation tìm kiếm
        animation_queue.append(self.animation_search(key))

        # Thêm nút
        self.create_node_and_rotate(key)

    def create_node_and_rotate(self, key):
        # Searching
        node = self.root

        # Chèn
        while True:
            is_left = key < node.key
            sub = node.left if is_left else node.right

            if sub is not None:
                node = sub
                continue

            sub = Node(key, Vector2(WIDTH // 2, 650))
            sub.parent = node
            if is_left:
                node.left = sub
            else:
                node.right = sub

            animation_queue.append(sub.animation_move())
            break

        check_rotate(node)

    def animation_search(self, key):
        "Hành động tìm kiếm trên cây nhị phân"

        if not self.root:
            return
            
        selection = self.root
        for _ in animation_pause(1):
            pygame.draw.circle(screen, RED, selection.position, 25, 3)
            yield None

        while selection is not None:
            if selection.key == key:
                for _ in animation_pause(0.8):
                    pygame.draw.circle(screen, GREEN, selection.position, 25, 5)
                    yield None
                return
            elif selection.key > key:
                selection = selection.left
            else:
                selection = selection.right

            for _ in animation_pause(0.8):
                pygame.draw.circle(screen, RED, selection.position, 25, 3)
                yield None

    def show_duplicate_message(self):
        # Hiển thị thông báo nếu số đã tồn tại
        message = "Số đã tồn tại, vui lòng nhập lại !"
        text_surface = font.render(message, True, RED)

        functor = lambda: screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT - 100))

        try:
            for _ in animation_repeat(3, functor):
                yield None
        except:
            pass

    def animate_node_to_position(self, node, final_x, final_y):
        """
        Hiệu ứng di chuyển nút từ vị trí ban đầu đến vị trí cuối cùng.
        """
        global delta_time

        step = 25 * delta_time  # Khoảng cách di chuyển mỗi khung hình
        vec = pygame.Vector2(final_x, final_y) - pygame.Vector2(node.x, node.y)
        vec = vec.normalize()
     
        # screen.fill(WHITE)
        # self.set_positions(self.root, WIDTH // 2, 50, 250)
        # self.draw(self.root)

        while node.y < final_y:
            node.x += vec.x * step
            node.y += vec.y * step
            pygame.draw.circle(screen, RED, (node.x, node.y), 20)
            text = font.render(str(node.key), True, WHITE)
            screen.blit(text, (node.x - text.get_width() // 2, node.y - text.get_height() // 2))
            yield None
        
        node.x, node_y = final_x, final_y
        yield None

    def delete(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self.delete(node.left, key)
        elif key > node.key:
            node.right = self.delete(node.right, key)
        else:
            if not node.left:
                temp = node.right
                node = None
                return temp
            elif not node.right:
                temp = node.left
                node = None
                return temp

            temp = self.min_value_node(node.right)
            node.key = temp.key
            node.right = self.delete(node.right, temp.key)

        if not node:
            return node

        node.update_height()
        balance = self.get_balance(node)

        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)

        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)

        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def draw(self):
        draw_root(self.root)

tree = AVL()    # type: ignore

def check_rotate(node):
    global tree

    node.update_height()
    parent = node.parent

    if node.height <= 2:
        if parent is not None:
            check_rotate(parent)
        return

    # Kiểm tra balance ở 'node'
    balance = node.get_balance()

    if balance > 1:     # Lệch trái
        if node.left.right is not None and node.right is not None and node.left.right.height > node.right.height:  # Cây con trái lệch phải
            animation_queue.append(animation_rotate_left(node.left, False))
        animation_queue.append(animation_rotate_right(node, True))
    elif balance < -1:  # Lệch phải
        if node.right.left is not None and node.left is not None and node.right.left.height > node.left.height:  # Cây con phải lệch trái
            animation_queue.append(animation_rotate_right(node.right, False))
        animation_queue.append(animation_rotate_left(node, True))
    elif node.parent is not None:
        check_rotate(node.parent)

def animation_rotate_right(node, on_top):
    node = node.rotate_right()
    node.update_height()
    if node.parent is None:
        tree.root = node
    else:
        node.parent.update_height()

    nodes = []
    node._make_nodes(nodes)
    positions = list((node.get_position(Vector2(WIDTH // 2, 50), 350) for node in nodes))

    # Animation rorate left
    for _ in animation_move(nodes, positions):
        yield None

    if on_top is True and node.parent is not None:
        check_rotate(node.parent)
    yield None

def animation_rotate_left(node, on_top):
    node = node.rotate_left()
    node.update_height()
    if node.parent is None:
        tree.root = node
    else:
        node.parent.update_height()

    nodes = []
    node._make_nodes(nodes)
    positions = list((node.get_position(Vector2(WIDTH // 2, 50), 350) for node in nodes))

    # Animation rorate left
    for _ in animation_move(nodes, positions):
        yield None

    if on_top is True and node.parent is not None:
        check_rotate(node.parent)
    yield None

# Main Loop

running = True
insert_value = ""
delete_value = ""
search_value = ""

# Đặt các ô nhập liệu gần cạnh dưới
input_box_insert = pygame.Rect(50, HEIGHT - 60, 160, 40)
button_box_insert = pygame.Rect(220, HEIGHT - 60, 100, 40)

input_box_delete = pygame.Rect(400, HEIGHT - 60, 160, 40)
button_box_delete = pygame.Rect(580, HEIGHT - 60, 100, 40)

input_box_search = pygame.Rect(750, HEIGHT - 60, 160, 40)
button_box_search = pygame.Rect(930, HEIGHT - 60, 100, 40)

active_insert = False
active_delete = False
active_search = False
search_triggered = False

search_message_displayed = False
search_message_time = 0  # Thời gian để hiển thị thông báo (tính bằng giây)

delete_message_displayed = False
delete_message_time = 0  # Thời gian để hiển thị thông báo xóa (tính bằng giây)
delete_message = ""

# Biến để theo dõi thời gian nhấp nháy con trỏ
cursor_blink_time = 0
cursor_blink_interval = 0.5  # Con trỏ nhấp nháy mỗi nửa giây
cursor_visible = True  # Define the cursor_visible variable before it's used

if __name__ == '__main__':
    while running:
        screen.fill(WHITE)

        tree.draw()
        run_animation()

        # Vẽ thanh ngang phía dưới
        pygame.draw.rect(screen, WHITE, (0, HEIGHT - 70, WIDTH, 70))

        # Vẽ các ô nhập liệu và nút
        pygame.draw.rect(screen, GRAY, input_box_insert, 2)
        txt_surface_insert = font.render(insert_value, True, BLACK)
        screen.blit(txt_surface_insert, (input_box_insert.x + 5, input_box_insert.y + 5))
        pygame.draw.rect(screen, RED, button_box_insert)
        button_label_insert = font.render("Chèn", True, WHITE)
        screen.blit(button_label_insert, (button_box_insert.x + 15, button_box_insert.y + 5))

        pygame.draw.rect(screen, GRAY, input_box_delete, 2)
        txt_surface_delete = font.render(delete_value, True, BLACK)
        screen.blit(txt_surface_delete, (input_box_delete.x + 5, input_box_delete.y + 5))
        pygame.draw.rect(screen, RED, button_box_delete)
        button_label_delete = font.render("Xoá", True, WHITE)
        screen.blit(button_label_delete, (button_box_delete.x + 15, button_box_delete.y + 5))

        pygame.draw.rect(screen, GRAY, input_box_search, 2)
        txt_surface_search = font.render(search_value, True, BLACK)
        screen.blit(txt_surface_search, (input_box_search.x + 5, input_box_search.y + 5))
        pygame.draw.rect(screen, RED, button_box_search)
        button_label_search = font.render("Tìm Kiếm", True, WHITE)
        screen.blit(button_label_search, (button_box_search.x + 15, button_box_search.y + 5))

        # Quản lý thời gian để con trỏ nhấp nháy
        current_time = time.time()
        if active_insert or active_delete or active_search:
            if current_time - cursor_blink_time > cursor_blink_interval:
                cursor_blink_time = current_time
                cursor_visible = not cursor_visible  # Thay đổi trạng thái con trỏ (hiển thị hoặc không)

        # Vẽ con trỏ nhấp nháy khi cần thiết
        if (active_insert and cursor_visible) or (active_delete and cursor_visible) or (active_search and cursor_visible):
            cursor_x = input_box_insert.x + 5 + font.size(insert_value)[0] if active_insert else input_box_delete.x + 5 + font.size(delete_value)[0] if active_delete else input_box_search.x + 5 + font.size(search_value)[0]
            pygame.draw.line(screen, BLACK, (cursor_x, input_box_insert.y + 5), (cursor_x, input_box_insert.y + 35), 2)  # Vẽ con trỏ

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_insert.collidepoint(event.pos):
                    active_insert = True
                    active_delete = False
                    active_search = False
                    search_value = ""  # Reset giá trị ô tìm kiếm
                elif input_box_delete.collidepoint(event.pos):
                    active_delete = True
                    active_insert = False
                    active_search = False
                    search_value = ""  # Reset giá trị ô tìm kiếm
                elif input_box_search.collidepoint(event.pos):
                    active_search = True
                    active_insert = False
                    active_delete = False
                else:
                    active_insert = active_delete = active_search = False

                if button_box_insert.collidepoint(event.pos):
                    if not insert_value.isdigit():  # Kiểm tra giá trị hợp lệ
                        insert_value = ""
                        continue

                    # if insert_value.isdigit():
                    tree.insert(int(insert_value))
                    insert_value = ""
                    search_message_displayed = False  # Ẩn thông báo khi có hành động chèn
                    search_triggered = False
                    delete_message_displayed = False

                if button_box_delete.collidepoint(event.pos):
                    if delete_value.isdigit():
                        node_to_delete = tree.search(tree.root, int(delete_value))
                        if node_to_delete:
                            tree.root = tree.delete(tree.root, int(delete_value))
                            delete_message = "Xóa Thành Công"
                            search_value = ""  # Reset giá trị ô tìm kiếm
                            tree.found_node = None  # Xoá trạng thái tìm kiếm
                        else:
                            delete_message = "Không Tìm Thấy Số Để Xoá"
                        delete_value = ""
                        delete_message_displayed = True
                        delete_message_time = time.time()
                        search_message_displayed = False
                        search_triggered = False

                if button_box_search.collidepoint(event.pos):
                    search_triggered = True
                    if search_value.isdigit():
                        tree.found_node = tree.search(tree.root, int(search_value))
                        if tree.found_node:
                            print(f"{tree.found_node.key}")
                        else:
                            print("")

            # Kiểm tra khi nhấn phím trong phần xử lý nhập liệu
            elif event.type == pygame.KEYDOWN:
                if active_insert:
                    if event.key == pygame.K_BACKSPACE:
                        insert_value = insert_value[:-1]
                    elif event.key == pygame.K_RETURN:  # Nhấn Enter để chèn
                        if insert_value.isdigit():
                            tree.insert(int(insert_value))
                            insert_value = ""
                            search_message_displayed = False
                            search_triggered = False
                            delete_message_displayed = False
                    else:
                        insert_value += event.unicode
                elif active_delete:
                    if event.key == pygame.K_BACKSPACE:
                        delete_value = delete_value[:-1]
                    elif event.key == pygame.K_RETURN:  # Nhấn Enter để xóa
                        if delete_value.isdigit():
                            node_to_delete = tree.search(tree.root, int(delete_value))
                            if node_to_delete:
                                tree.root = tree.delete(tree.root, int(delete_value))
                                delete_message = "Xóa Thành Công"
                                search_value = ""  # Reset giá trị ô tìm kiếm
                                tree.found_node = None  # Xoá trạng thái tìm kiếm
                            else:
                                delete_message = "Không Tìm Thấy Số Để Xoá"
                        delete_value = ""  # Reset ô nhập liệu sau khi xóa
                        delete_message_displayed = True
                        delete_message_time = time.time()  # Cập nhật thời gian hiển thị thông báo
                        search_message_displayed = False
                        search_triggered = False
                    else:delete_value += event.unicode
                elif active_search:
                    if event.key == pygame.K_BACKSPACE:
                        search_value = search_value[:-1]
                    elif event.key == pygame.K_RETURN:  # Nhấn Enter để tìm kiếm
                        if search_value.isdigit():
                            tree.found_node = tree.search(tree.root, int(search_value))
                            if tree.found_node:
                                print(f"{tree.found_node.key}")
                            else:
                                print("Không tìm thấy")
                        delete_message_displayed = False
                        search_triggered = True
                    else:
                        search_value += event.unicode

        # Hiển thị thông báo tìm kiếm
        if search_triggered:
            if tree.found_node:
                pygame.draw.circle(screen, YELLOW, (tree.found_node.x, tree.found_node.y), 25, 5)
                text_found = font.render("Tìm Thấy", True, BLACK)
                screen.blit(text_found, (WIDTH // 2 - text_found.get_width() // 2, HEIGHT - 100))
                search_message_displayed = True
                search_message_time = time.time()  # Cập nhật thời gian khi tìm thấy
            else:
                text_not_found = font.render("Không tìm thấy", True, RED)
                screen.blit(text_not_found, (WIDTH // 2 - text_not_found.get_width() // 2, HEIGHT - 100))
                search_message_displayed = True
                search_message_time = time.time()  # Cập nhật thời gian khi không tìm thấy

        # Nếu đã hiển thị thông báo trong quá khứ và thời gian hiện tại đã quá lâu, ẩn thông báo
        if search_message_displayed and (time.time() - search_message_time) > 2:  # 2 giây
            search_message_displayed = False
            search_triggered = False

        if delete_message_displayed:
            delete_text = font.render(delete_message, True, BLACK if delete_message == "Xóa Thành Công" else RED)
            screen.blit(delete_text, (WIDTH // 2 - delete_text.get_width() // 2, HEIGHT - 100))

        if delete_message_displayed and (time.time() - delete_message_time) > 2:  # 2 giây
            delete_message_displayed = False

        pygame.display.flip()
        delta_time = clock.tick(60) / 1000