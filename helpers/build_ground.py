from math import pi
import random

from helpers.vector import Vector3

from engine.model.material.material import Material

from engine.model.polygon.face import Face
from engine.model.polygon.vertex import Vertex
from engine.model.polygon.polygon import Polygon


def build_ground(models, camera, face_width=40, min_x=-20, min_y=-20, max_x=20, max_y=20, amp=10):
    ground_offset = random.randint(0, 100000000)
    seed1 = random.randint(0, 100000000)
    seed2 = random.randint(0, 100000000)

    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            freq, bias = pi / 8, -9.9
            height00 = noise(x * freq + ground_offset, y * freq) * amp + bias
            height01 = noise(x * freq + ground_offset, (y + 1) * freq) * amp + bias
            height10 = noise((x + 1) * freq + ground_offset, y * freq) * amp + bias
            height11 = noise((x + 1) * freq + ground_offset, (y + 1) * freq) * amp + bias

            dx00 = noise(x * 1 + seed1, y * 1) * face_width * 20
            dy00 = noise(x * 1 + seed2, y * 1) * face_width * 20
            dx01 = noise(x * 1 + seed1, (y + 1) * 1) * face_width * 20
            dy01 = noise(x * 1 + seed2, (y + 1) * 1) * face_width * 20
            dx10 = noise((x + 1) * 1 + seed1, y * 1) * face_width * 20
            dy10 = noise((x + 1) * 1 + seed2, y * 1) * face_width * 20
            dx11 = noise((x + 1) * 1 + seed1, (y + 1) * 1) * face_width * 20
            dy11 = noise((x + 1) * 1 + seed2, (y + 1) * 1) * face_width * 20

            material = Material({"Kd": [0, 150 / 255, 0], "d": 1})

            obj_pos = Vector3(x * face_width, y * face_width, 0)

            triangle1 = Polygon([], {})
            triangle2 = Polygon([], {})

            if random.random() < 0.5:
                triangle1.faces.append(Face([Vertex(Vector3(dx00, dy00, height00), obj_pos),
                                             Vertex(Vector3(dx01, dy01 + face_width, height01), obj_pos),
                                             Vertex(Vector3(face_width + dx10, dy10, height10), obj_pos)
                                             ], material))
                triangle2.faces.append(
                    Face([Vertex(Vector3(face_width + dx11, face_width + dy11, height11), obj_pos),
                          Vertex(Vector3(dx01, face_width + dx01, height01), obj_pos),
                          Vertex(Vector3(face_width + dx10, dx10, height10), obj_pos)
                          ], material))
            else:
                triangle1.faces.append(Face([Vertex(Vector3(dx01, face_width + dx01, height01), obj_pos),
                                             Vertex(Vector3(dx00, dx00, height00), obj_pos),
                                             Vertex(Vector3(face_width + dx11, face_width + dy11, height11),
                                                    obj_pos)
                                             ], material))
                triangle2.faces.append(Face([Vertex(Vector3(face_width + dx10, dx10, height10), obj_pos),
                                             Vertex(Vector3(dx00, dx00, height00), obj_pos),
                                             Vertex(Vector3(face_width + dx11, face_width + dy11, height11),
                                                    obj_pos)
                                             ], material))

            triangle1.set_camera(camera)
            triangle2.set_camera(camera)

            models[models._model_id] = triangle1
            models[models._model_id + 1] = triangle2
            models._model_id += 2
