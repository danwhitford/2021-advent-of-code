from aoc2021.day24 import ALU

def test_read():
    s = '''inp w
        add z w
        mod z 2
        div w 2
        add y w
        mod y 2
        div w 2
        add x w
        mod x 2
        div w 2
        mod w 2'''
    
    i = ALU.read_program(s)
    assert 11 == len(i)
    assert ['inp', 'w'] == i[0]

def test_easy():
    s = '''inp x
        mul x -1'''
    alu = ALU()
    alu.load_program(s)
    alu.execute([10])
    assert -10 == alu.environment['x'] 

def test_example():
    s = '''inp z
        inp x
        mul z 3
        eql z x'''
    alu = ALU()
    alu.load_program(s)
    alu.execute([10, 30])
    assert alu.environment['z'] == 1
    assert not alu.validate_model_number((10, 30))
    assert alu.validate_model_number((10, 35))
    
def test_example2():
    s = '''inp w
        add z w
        mod z 2
        div w 2
        
        add y w
        mod y 2
        div w 2
        add x w
        mod x 2
        div w 2
        mod w 2'''
    alu = ALU()
    alu.load_program(s)
    alu.execute([10])
    assert alu.environment['z'] == 0
    assert alu.environment['w'] == 1

