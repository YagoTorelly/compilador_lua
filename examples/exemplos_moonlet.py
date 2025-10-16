def obter_exemplo(tipo='completo'):
    
    exemplos = {
        'completo': '''
-- Exemplo completo de funcionalidades Moonlet
local contador = 0
local nome = "Moonlet"

function saudacao(usuario)
    if usuario then
        print("Olá, " .. usuario .. "!")
    else
        print("Olá, visitante!")
    end
end

function contar_ate(limite)
    local i = 1
    while i <= limite do
        print("Contando: " .. i)
        i = i + 1
    end
end

-- Chamadas de função
saudacao(nome)
contar_ate(3)

-- Estrutura condicional
if contador == 0 then
    print("Contador zerado")
else
    print("Contador: " .. contador)
end
        ''',
        
        'simples': '''
local x = 10
if x > 5 then
    print("x é maior que 5")
end
        ''',
        
        'loops': '''
for i = 1, 5 do
    print(i)
end

local j = 1
while j <= 3 do
    print("j = " .. j)
    j = j + 1
end
        '''
    }
    
    return exemplos.get(tipo, exemplos['completo']).strip()
