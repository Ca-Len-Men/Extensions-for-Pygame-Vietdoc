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

- Lớp `Vector` : mô phỏng `vector` trong mặt phẳng ( hệ trục tọa độ `Oxy` ).

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

| Method | Chức năng | Ghi chú |
|:--------------|:---------:|:--------|
| **def** \__init__(self, `x`: *float*, `y`: *float*) | Khởi tạo `Vector` | |
| **def** setxy(self, `__x`: *float*, `__y`: *float*) -> None | Gán thuộc tính `x, y` | **Đáng chú ý** : mọi thay đổi trên `x, y` đều phải được thông qua hàm này ( bao gồm **set property** ) ! |
| **def** set(self, `source`: *Union[Tuple[float, float], List[float], Vector]*) -> None | Gán thuộc tính `x, y` | |
| **def** copy(self) -> *Vector* | Trả về bản sao mới | |
| **def** magnitude(self, `other`: *Vector*) -> *float* | Khoảng cách giữa hai `Vector` | |
| **def** normalize(self) -> *Vector* | Trả về `Vector` mới cùng hướng ( góc bằng nhau ) nhưng độ dài bằng `1` | |
| **def** lerp(self, `target`: *Vector*, `delta`: *float*) -> bool | Tịnh tiến đến `target` một khoảng `delta` | |

</details>

---

### Module `frect.py`

- Updating ...

### Module `fdraw.py`

- Updating ...

### Module `color.py`

- Updating ...

### Module `imagine.py`

- Updating ...
