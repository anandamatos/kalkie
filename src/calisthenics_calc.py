def fibonacci_sequence(n, min_val=1):
    """Gera sequência Fibonacci até atingir n valores, começando no primeiro valor >= min_val."""
    if n <= 0:
        return []
    a, b = 1, 1
    sequence = []
    while a < min_val:
        a, b = b, a + b
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence

def redistribute_small_values(block, subblocks):
    """Redistribui valores <=5 combinando-os com elementos adjacentes."""
    if all(x > 5 for x in subblocks) or len(subblocks) == 1:
        return subblocks
    
    result = []
    temp = 0
    for val in subblocks:
        if val <= 5:
            temp += val
        else:
            if temp > 0:
                if result:
                    result[-1] += temp
                else:
                    result.append(temp)
                temp = 0
            result.append(val)
    
    if temp > 0:
        if result:
            result[-1] += temp
        else:
            result.append(temp)
    
    if result and result[0] <= 5 and len(result) > 1:
        result[1] += result[0]
        result = result[1:]
    
    if any(x <= 5 for x in result) and len(result) > 1:
        return redistribute_small_values(block, result)
    
    if sum(result) != block:
        diff = block - sum(result)
        result[-1] += diff
    
    return result

def adjust_blocks(blocks, min_val=6):
    """Garante que todos os blocos principais tenham pelo menos min_val."""
    total = sum(blocks)
    n = len(blocks)
    
    if total < min_val * n:
        return blocks
    
    adjusted = blocks[:]
    
    for i in range(n-1, -1, -1):
        if adjusted[i] < min_val:
            needed = min_val - adjusted[i]
            for j in range(i):
                if adjusted[j] > min_val and adjusted[j] >= needed:
                    adjusted[j] -= needed
                    adjusted[i] = min_val
                    break
            else:
                if adjusted[0] >= needed:
                    adjusted[0] -= needed
                    adjusted[i] = min_val
    
    if all(x >= min_val for x in adjusted):
        return adjusted
    
    for i in range(n-1, -1, -1):
        if adjusted[i] < min_val:
            needed = min_val - adjusted[i]
            for j in range(n):
                if j != i and adjusted[j] >= needed:
                    adjusted[j] -= needed
                    adjusted[i] += needed
                    break
    
    return adjusted

def calculate_blocks(total, num_blocks, num_subblocks):
    fib_blocks = fibonacci_sequence(num_blocks, min_val=2)
    sum_fib_blocks = sum(fib_blocks)
    
    blocks = [round((f/sum_fib_blocks) * total) for f in fib_blocks]
    
    diff = total - sum(blocks)
    blocks[-1] += diff
    
    blocks.sort(reverse=True)
    blocks = adjust_blocks(blocks, min_val=6)
    
    subblocks_table = []
    for i, block in enumerate(blocks):
        current_subblocks = max(1, num_subblocks - i)
        min_sub_val = 1 if block < 15 else 2
        fib_subs = fibonacci_sequence(current_subblocks, min_val=min_sub_val)
        
        sum_fib_subs = sum(fib_subs) or 1
        subblocks = [round((f/sum_fib_subs) * block) for f in fib_subs]
        
        diff = block - sum(subblocks)
        if subblocks:
            subblocks[-1] += diff
        
        if len(subblocks) > 1:
            subblocks = redistribute_small_values(block, subblocks)
        
        subblocks.sort(reverse=True)
        subblocks_table.append(subblocks)
    
    return blocks, subblocks_table

def automatic_training(total):
    """Calcula automaticamente os parâmetros para um treino baseado no total de repetições."""
    # Definir número de blocos baseado no total
    if total <= 50:
        num_blocks = 3
    elif total <= 100:
        num_blocks = 4
    elif total <= 200:
        num_blocks = 5
    elif total <= 300:
        num_blocks = 6
    else:
        num_blocks = 7
    
    # Definir número de subblocos baseado no total
    if total <= 50:
        num_subblocks = 3
    elif total <= 100:
        num_subblocks = 4
    elif total <= 200:
        num_subblocks = 5
    elif total <= 300:
        num_subblocks = 6
    else:
        num_subblocks = 7
    
    print(f"Modo automático: {total} repetições, {num_blocks} blocos, {num_subblocks} subblocos")
    return calculate_blocks(total, num_blocks, num_subblocks)

def format_output(total, blocks, subblocks):
    print(f"\\nDESAFIO {total}x")
    for i in range(len(blocks)):
        sub_str = ', '.join(map(str, subblocks[i]))
        print(f"{blocks[i]}x = [{sub_str}]")

def calculadora_calistenia():
    """Função interativa para calcular divisão de exercícios de calistenia."""
    print("\\n" + "="*50)
    print("🧮 CALCULADORA DE CALISTENIA")
    print("="*50)
    
    total = int(input("Valor total de repetições (0 para modo automático): "))
    
    if total == 0:
        auto_total = int(input("Total de repetições para o treino automático: "))
        blocks, subblocks = automatic_training(auto_total)
        format_output(auto_total, blocks, subblocks)
    else:
        num_blocks = int(input("Número de blocos principais: "))
        num_subblocks = int(input("Número de subblocos por bloco: "))
        blocks, subblocks = calculate_blocks(total, num_blocks, num_subblocks)
        format_output(total, blocks, subblocks)
    
    input("\\nPressione Enter para continuar...")