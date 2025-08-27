extends CharacterBody3D

var ai_model
var memory = []
var health = 100

func _ready():
    ai_model = preload("res://ai_models/model1.py") # يمكن تغييره لكل لاعب

func _process(delta):
    var action = ai_model.get_action(self, memory)
    perform_action(action)
    update_memory(action)

func perform_action(action):
    # مثال: الحركة، الهجوم، الذهاب للعلاج، إلخ
    pass

func update_memory(action):
    memory.append({
        "action": action,
        "result": check_result(action)
    })

func check_result(action):
    # يرجع تقييم: نجح أم لم ينجح
    pass