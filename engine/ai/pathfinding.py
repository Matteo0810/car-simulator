from helpers.dotenv import get_env
from helpers.ordered_list import OrderedList
from helpers.utils import sign
from helpers.vector import Vector2
from world.car import Car

TIME_STEP = 0.5
FORESEE_TIME = 2


def unpack_actions_flag(actions_flag, speed_limit):
    if actions_flag & 0b11100 == 0b00000:
        steer_angle = -0.6
    elif actions_flag & 0b11100 == 0b00100:
        steer_angle = -0.3
    elif actions_flag & 0b11100 == 0b01000:
        steer_angle = -0.1
    elif actions_flag & 0b11100 == 0b01100:
        steer_angle = 0.6
    elif actions_flag & 0b11100 == 0b10000:
        steer_angle = 0.3
    elif actions_flag & 0b11100 == 0b10100:
        steer_angle = 0.1
    else:
        steer_angle = 0
    
    if actions_flag & 0b11 != 0b11:
        braking = False
        if actions_flag & 0b11 == 0b01:
            wheel_speed = -speed_limit / 2
        elif actions_flag & 0b11 == 0b10:
            wheel_speed = speed_limit
        else:
            wheel_speed = 0
    else:
        wheel_speed = 0
        braking = True
    
    return steer_angle, wheel_speed, braking


def find_path(scene, car, next_path, current_path):
    has_priority = current_path.intersection.has_priority(current_path, next_path, car.world)
    
    node_source = {"parent": None, "score": 0, "actions_flag": 0, "time": 0, "on_next_path": False,
                   "changed_path": False,
                   "car_position": car.position, "car_velocity": car.velocity.length(), "car_angle": car.angle}
    
    start_pos = car.position
    
    node_value = lambda node: node["score"]  # + node["dev_score"]
    
    nodes = OrderedList(lambda n1, n2: node_value(n1) - node_value(n2), [node_source])
    
    # chaque noeud (ou instant) posséde un score basé sur la distance à la route, l'avancée sur la route et la proximité
    # des obstacles dangereux à court terme
    
    # les noeuds sont caractérisés par un choix (flag)
    
    actions = []
    
    loops = 0
    
    # simulation rapide du déplacement de la voiture et de son environnement
    while True:
        loops += 1
        
        parent = nodes.min()
        
        if loops > 20 or parent["time"] == FORESEE_TIME:
            
            while parent["parent"]["parent"]:
                actions.append(parent)
                parent = parent["parent"]
                # scene.add_debug_dot(parent["car_position"], (200, 200, 0))
            
            actions.append(parent)
            actions.reverse()
            
            return actions
        
        nodes.remove(parent)
        
        for actions_flag in range(0b11001):
            # if actions_flag & 0b11 == 0b11:
            #    continue
            
            node = {"parent": parent, "actions_flag": actions_flag, "time": parent["time"] + TIME_STEP}
            score = 0
            
            position = parent["car_position"]
            velocity = parent["car_velocity"]
            angle = parent["car_angle"]
            path = next_path if parent["on_next_path"] else current_path
            
            steer_angle, wheel_speed, braking = unpack_actions_flag(actions_flag, path.road.speed_limit)
            vel_diff = 0
            
            if braking:
                vel_diff = -velocity * 0.5
            else:
                if wheel_speed > 0 and velocity < path.road.speed_limit:
                    if sign(velocity) != sign(wheel_speed):
                        vel_diff = car.model.acceleration * TIME_STEP
                    else:
                        vel_diff = car.model.acceleration * TIME_STEP
                if wheel_speed < 0 and velocity > -path.road.speed_limit:
                    if sign(velocity) != sign(wheel_speed):
                        vel_diff = -car.model.acceleration * TIME_STEP
                    else:
                        vel_diff = -car.model.acceleration * TIME_STEP

            # B, C, D, E = 0.01, 1.7, -100, -1.2
            # x = (velocity + vel_diff) * 25
            # f = D * sin(C * atan(B * x/2 - E * (B * x/2 - atan(B * x/2))))
            # angle -= f * steer_angle / 150 * sign(velocity) * 1.5
            angle += velocity * steer_angle * TIME_STEP / 7
            
            velocity += vel_diff - 2 * sign(velocity)
            
            l_position = position
            position += Vector2.of_angle(angle, velocity) * TIME_STEP
            
            node["on_next_path"] = (parent["on_next_path"] or path.end.distance(position) < 5) and has_priority
            node["changed_path"] = not parent["on_next_path"] and node["on_next_path"]
            
            path = next_path if node["on_next_path"] else current_path
            
            if not node["changed_path"] and not parent["changed_path"]:
                score += path.distance(position)
            else:
                score += path.distance(position)
            
            if not has_priority:
                goal = (path.end - path.direction * get_env("ROAD_WIDTH") * 0.8)
                score += goal.distance(position)
                if goal.distance(position) < goal.distance(position + Vector2.of_angle(angle, velocity) / 2):
                    score += velocity
            else:
                score += path.end.distance(position)
                score -= min(10, abs(velocity))
            
            if not node["on_next_path"]:
                score += current_path.end.distance(next_path.end)
            
            for collideable in car.world.collideables:
                if collideable == car:
                    continue
                
                nearest_hitbox_point = collideable.nearest_hitbox_point(position)
                
                if nearest_hitbox_point:
                    if isinstance(collideable, Car):
                        nearest_hitbox_point += collideable.velocity * node["time"]
                    
                    dist = nearest_hitbox_point.distance(position)
                    
                    if dist <= car.model.diagonal and node["time"] < 1:
                        score += 10000000
                    # if dist <= car.model.diagonal:
                    #    score += (car.model.diagonal - dist)
            
            node["score"] = score
            node["car_position"] = position
            node["car_velocity"] = velocity
            node["car_angle"] = angle
            nodes.insert(node)
