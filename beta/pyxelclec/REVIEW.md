<h1 align="center">🐍 PYXEL 1.0.0 REVIEW 🐍</h1>


<h1 align="center">🎮 Giới thiệu sơ đồ 🎮</h1>
<img align="right" width="256px" height="256px" src="../../Assets/code-review.png">

### Cây thư mục dự án

```
pyxelclec
+----geo
|       \   __init__.py
|       \   fmath.py
|       \   fvector.py
|       \   frect.py
|       \   fdraw.py
|       \   color.py
|       \   imagine.py
|
+----model
|       +----components
|       |       \   __init__.py
|       |       \   ccollider.py
|       |       \   cinput.py
|       |       \   cscripts.py
|       |       \   csprite.py
|       |
|       \   __init__.py
|       \   component.py
|       \   entity.py
|       \   canvas.py
|       \   base.py
|
+----scripts
|       \   __init__.py
|       \   timing.py
|       \   button.py
|       \   text.py
|
\   __init__.py
\   __flag__.py
\   __info__.py
\   assets.py
\   pattern.py
\   scene.py
```

---

<h1 align="center"><a name="pyxelclec.geo"></a>📑 Giới thiệu <code>pyxelclec.geo</code> 📑</h1>

<details>
<summary><a name="fmath.py"></a><h3>Module <code>fmath.py</code></h3></summary>

- Triển khai các hàm toán học cơ bản :

| Các biến và hàm | Chức năng | Ghi chú |
|:--------------|:---------:|:--------|
| APPROXIMATE = 0.000_000_001 | Sai số có thể chấp nhận | |
| PI = 3.14159_26535_89793 | Giá trị xấp xỉ của `pi` | |
| **def** _radians(`__degrees`: *float*) -> *float* | Đổi từ `degrees` sang `radians` | |
| **def** _degrees(`__radians`: *float*) -> float | Đổi từ `radians` sang `degrees` | |
| **def** relative_compare(`a`: *float*, `b`: *float*) -> *bool* | So sánh bằng hai kiểu `float` | `abs(a - b) <= APPROXIMATE` thì được xem là `a == b` |
| **def** angle(`vec_x`: *float*, `vec_y`: *float*) -> *float* | Tính góc của `vector(x, y)` | Giá trị trả về trong đoạn `[0, 360]` |
| **def** vector(`__degrees`: *float*) -> Tuple[*float*, *float*] | Trả về giá trị `x, y` của `vector` độ dài `1` có góc bằng `__degrees` | |
| **def** magnitude(`x`: *float*, `y`: *float*) -> *float* | Tính độ dài `vector(x, y)` | |
| **def** lerp(`current`: *float*, `target`: *float*, `delta`: *float*) -> *float* | Tịnh tiến từ `current` đến `target` một khoảng `delta` | |

</details>

---

<details>
<summary><a name="fvector.py"></a><h3>Module <code>fvector.py</code></h3></summary>

- Module `fvector` chủ yếu xây dựng `Vector` trong mặt phẳng để ứng dụng trong trò chơi, gồm các lớp cần thiết sau :
    - [Vector](#Vector)
    - [WeakrefMethod](#WeakrefMethod)
    - [Delegate](#Delegate)
    - [VectorListener](#VectorListener)
    - [VectorDependent](#VectorDependent)

---

- <a name="Vector"></a> Lớp <code>Vector</code> : mô phỏng <code>vector</code> trong mặt phẳng ( hệ trục tọa độ <i>Oxy</i> ). Một <code>Vector</code> có thể được xem như một điểm, hoặc một hướng trong mặt phẳng.

| Attributes | Chức năng | Ghi chú |
|:--------------|:---------:|:--------|
| `__x`: *float* | Giá trị tại trục `Ox` | |
| `__y`: *float* | Giá trị tại trục `Oy` | |
| `x`: *float* (get/set) | Giá trị tại trục `Ox` | |
| `y`: *float* (get/set) | Giá trị tại trục `Oy` | |
| `angle`: *float* (get/set) | Góc của `Vector` ( `degrees` ) | Giá trị luôn nằm trong đoạn `[0, 360]` |
| `tup`: *Tuple[float, float]* (get/set) | `Vector` có kiểu `tuple` | |
| `tup_int`: *Tuple[int, int]* (get) | `Vector` *nguyên* có kiểu `tuple` | |

- Hỗ trợ các phương thức tính toán với `Vector`.

| Methos | Chức năng | Ghi chú |
|:--------------|:---------:|:--------|
| **def** <span style="color:purple;"><strong>\_\_init__</strong></span>(self, `x`: *float*, `y`: *float*) | Khởi tạo `Vector` | |
| **def** setxy(self, `__x`: *float*, `__y`: *float*) | Gán thuộc tính `x, y` | **Đáng chú ý** : mọi thay đổi trên `x, y` đều phải được thông qua hàm này ( bao gồm **set property** ) ! |
| **def** set(self, `source`: *Union[Tuple[float, float], List[float], Vector]*) | Gán thuộc tính `x, y` | |
| **def** copy(self) -> *Vector* | Trả về bản sao mới | |
| **def** magnitude(self, `other`: *Vector*) -> *float* | Khoảng cách giữa hai `Vector` | |
| **def** normalize(self) -> *Vector* | Trả về `Vector` mới cùng hướng ( góc bằng nhau ) nhưng độ dài bằng `1` | |
| **def** lerp(self, `target`: *Vector*, `delta`: *float*) -> bool | Tịnh tiến đến `target` một khoảng `delta` | |
| `__add__`, `__iadd__`, `__sub__`, `__isub__`, `__mul__`, `__imul__`, `__truediv__`, `__itruediv__`, `__floordiv__`, `__ifloordiv__`, `__abs__`, `__eq__`, `__ne__`, `__neg__`, `__getitem__`, `__setitem__` | Sử dụng phương thức bằng toán tử | |
| `__init__`, `__str__`, `__repr__`, `__copy__`, `__len__`, `__iter__`, `__float__`, `__bool__` | Dunder method | |

---

- <a name="WeakrefMethod"></a> Lớp <code>WeakrefMethod</code> : tham chiếu yếu đến các <i>bounded method</i> ( <code>weakref.WeakMethod</code>, xem thêm module <a href="https://docs.python.org/3/library/weakref.html">weakref</a> ). Một `WeakrefMethod` bị xem là "chết" nếu <i>bounded method</i> không còn vật chủ ( hoặc <code>\_\_call__</code> trả về <i>False</i> ).

| Attributes và Methods | Chức năng | Ghi chú |
|:--------------|:---------:|:--------|
| `__weakref_bounded_method`: `WeakMethod` | Tham chiếu yếu đến *bounded method* | |
| **def** <span style="color:purple;"><strong>\_\_init__</strong></span>(self, `__bounded_method`: *Callable[[...], None]*) | Khởi tạo | *Lưu ý* : định dạng `callable` nhận vào là `def xxx(*args) -> None` |
| **def** <span style="color:purple;"><strong>\_\_call__</strong></span>(self, *`args`) -> *bool* | Gọi đến *bounded method* nhận được lúc khởi tạo ( nếu vật chủ còn tồn tại ) | Trả về `False` nếu vật chủ bị thu gôm rác |

---

- <a name="Delegate"></a> Lớp <code>Delegate</code> : lưu trữ nhiều `WeakrefMethod` trong một `set` ( lưu nhiều *bounded method* ), trong lúc gọi đến các *bounded method*, nếu phát hiện có `WeakrefMethod` đã "chết", xóa chúng khỏi tập lưu trữ.

| Attributes và Methods | Chức năng | Ghi chú |
|:--------------|:---------:|:--------|
| `_weakref_methods`: *Set[WeakrefMethod]* | Tập lưu trữ | |
| **def** <span style="color:purple;"><strong>\_\_init__</strong></span>(self) | Khởi tạo | |
| **def** add(self, `__weakref_bounded_method`: *WeakrefMethod*) | Thêm một `WeakrefMethod` vào tập lưu trữ | |
| **def** call(self, *`args`) | Gọi đến toàn bộ *bounded method* mà nó lưu | Thực hiện cùng lúc "call" `WeakrefMethod` và kiểm tra, `WeakrefMethod` đã "chết" thì xóa nó khỏi tập lưu trữ. |

---

- <a name="VectorListener"></a> Lớp <code>VectorListener</code> : kế thừa từ <a href="#Vector">Vector</a>, hỗ trợ kích hoạt các hành động khi xảy ra sự thay đổi trên đó ( cụ thể là thay đổi giá trị <code>x, y</code> ).

| Attributes và Methods | Chức năng | Ghi chú |
|:--------------|:---------:|:--------|
| `__delegate`: *Delegate* | Lưu các hành động, sẽ kích hoạt khi sự thay đổi xảy ra | |
| **def** <span style="color:purple;"><strong>\_\_init__</strong></span>(self, `__x`: *float*, `__y`: *float*) | Khởi tạo | Override |
| **def** setxy(self, `__x`: *float*, `__y`: *float*) | Thay đổi giá trị `x, y` | Override |
| **def** add_listener(self, `__weakref_method`: WeakrefMethod) | Thêm một hành động | |
| **def** only_set(self, `source`: *Vector*) | Thay đổi giá trị `x, y` mà không kích hoạt các hành động | |

---

- <a name="VectorDependent"></a> Lớp <code>VectorDependent</code> : kế thừa từ <code>Vector</code>, <code>VectorDependend</code> phụ thuộc tương đối vào một <code>Vector</code> khác "một khoảng <code>Vector</code>". Nghĩa là khi nó cách "một khoảng" so với <code>Vector</code> mà nó tham chiếu đến, nếu <code>Vector</code> đó bị thay đổi, chính nó sẽ bị thay đổi và cách đúng "một khoảng" so với <code>Vector</code> đó.
    - Nếu nó không tham chiếu đến `Vector` nào khác, chức năng của nó không khác `Vector` thông thường.
    - Những `Vector` mà nó có thể tham chiếu đến là `Vector, VectorListener, VectorDependent` ngoại trừ chính nó.

| Attributes và Methods | Chức năng | Ghi chú |
|:--------------|:---------:|:--------|
| `__ref_vector`: *Union[Vector, VectorListener, VectorDependent]* | Tham chiếu đến `Vector` khác | Tôi không tưởng tượng nổi chuyện gì sẽ xảy ra khi nó tham chiếu đến chính nó đâu 😧 |
| `x`: *float* (get) | Giá trị tại trục `Ox` | Override |
| `y`: *float* (get) | Giá trị tại trục `Oy` | Override |
| **def** <span style="color:purple;"><strong>\_\_init__</strong></span>(self, `__x`: *float*, `__y`: *float*, `__ref_vector`: *Vector* = *None*) | Khởi tạo | Override |
| **def** setxy(self, `__x`: *float*, `__y`: *float*) | Thay đổi giá trị `x, y` | Override |
| **def** set_ref(self, `__ref_vector`: *Vector*) | Gán tham chiếu | Bạn chỉ nên gọi hàm này duy nhất một lần mỗi `instance` nếu chưa gán lúc khởi tạo |

</details>

---


<details>
<summary><a name="frect.py"></a><h3>Module <code>frect.py</code></h3></summary>

- Module `frect` chủ yếu mô phỏng hình chữ nhật trong mặt phẳng ( hệ tọa độ `Oxy` ).
- Hình chữ nhật được xác định bằng vị trí `top left` ( là góc dưới bên trái trong hệ tọa độ `Oxy`, hoặc góc trên bên trái đối với màn hình ứng dụng ) và kích thước `width height` ( chiều ngang và chiều dọc ).
- Thường dùng để căn chỉnh vị trí phù hợp, xác định va chạm, ... :
    - [StructRect](#StructRect)
    - [Rect](#Rect)

---

- <a name="StructRect"></a> Lớp <code>StructRect</code> : là hình chữ nhật được xác định bởi `top left` và `width height`.

| Attributes và Methods | Chức năng | Ghi chú |
|:--------------|:---------:|:--------|
| `_position`: *Vector* | Vị trí `top left` | |
| `_size`: *Vector* | Kích thước `width height` | |
| `size`: *Vector* (get/set) | Kích thước hình chữ nhật | Mọi thay đổi trên `_size` đều phải thông qua `property setter` của `size` |
| `w`: *float* (get/set) | Chiều ngang hình chữ nhật | |
| `h`: *float* (get/set) | Chiều dọc hình chữ nhật | |
| `topleft`: *Vector* (get/set) | | Mọi thay đổi trên `_position` đều phải thông qua `property setter` của `topleft`. |
| `topright`: *Vector* (get/set) | ... | |
| `bottomleft`: *Vector* (get/set) | ... | |
| `bottomright`: *Vector* (get/set) | ... | |
| `center`: *Vector* (get/set) | ... | |
| `midtop`: *Vector* (get/set) | ... | |
| `midbottom`: *Vector* (get/set) | ... | |
| `midleft`: *Vector* (get/set) | ... | |
| `midright`: *Vector* (get/set) | ... | |
| `midx`: *float* (get/set) | Hoặc `midtop.x` | |
| `midy`: *float* (get/set) | Hoặc `midleft.y` | |
| **def** <span style="color:purple;"><strong>\_\_init__</strong></span>(self, `size`: *Vector*, position: *Vector* = *None*) | Khởi tạo | Nếu `position is None`, mặc định `topleft = Vector.zero()` |
| **def** collide_point(self, `point`: *Vector*) -> *bool* | Kiểm tra `point` có nằm trên `StructRect` không ( bao gồm viền ) | |

---

- <a name="Rect"></a> Lớp <code>Rect</code> : kế thừa từ <code>StructRect</code>, cho phép thêm các hành động khi có sự thay đổi trên vị trí hoặc kích thước của nó.

| Attributes và Methods | Chức năng | Ghi chú |
|:--------------|:---------:|:--------|
| **def** <span style="color:purple;"><strong>\_\_init__</strong></span>(self, `size`: *Vector*, `position`: *Vector* = *None*) | Khởi tạo | Override |
| **def** size_listener(self, `__listener`: *WeakrefMethod*) | Thêm hành động khi kích thước thay đổi | |
| **def** pos_listener(self, `__listener`: *WeakrefMethod*) | Thêm hành động khi vị trí thay đổi | |
| **def** only_set_size(self, `__size`: *Vector*) | Chỉ thay đổi kích thước, không kích hoạt hành động | |
| **def** only_set_topleft(self, `__topleft`: *Vector*) | Chỉ thay đổi vị trí, không kích hoạt hành động | |

</details>

---

### Module `fdraw.py`

- Updating ...

### Module `color.py`

- Updating ...

### Module `imagine.py`

- Updating ...
