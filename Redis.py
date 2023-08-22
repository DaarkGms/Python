import redis
import os 

class TaskManager:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.task_counter_key = 'task_counter'
        self.last_task_id = int(self.redis_client.get(self.task_counter_key) or 0)

    def add_task(self, description): 
        self.last_task_id += 1
        task_id = self.last_task_id  
        self.redis_client.set(f'task:{task_id}', description)
        print(f'Tarefa {task_id} adicionada com sucesso.')

        self.redis_client.set(self.task_counter_key, self.last_task_id)  

    def listar_tarefas(self):
     task_ids = self.redis_client.keys('task:*')
     sorted_task_keys = sorted(task_ids, key=lambda x: int(x.decode('utf-8').split(':')[1]))

     for task_key in sorted_task_keys:
        task_id = task_key.decode('utf-8').split(':')[1]
        description = self.redis_client.get(task_key).decode('utf-8')
        print(f'ID da tarefa: {task_id}; Descrição: {description}')


    def remove_tarefa(self, task_id):
        task_key = f'task:{task_id}'
        if self.redis_client.exists(task_key):
            self.redis_client.delete(task_key)
            print(f'Tarefa com ID {task_id} removida com sucesso.')
            if int(task_id) == self.last_task_id:
                self.last_task_id -= 1
                self.redis_client.set(self.task_counter_key, self.last_task_id)  # Atualize o contador
        else:
            print(f'Tarefa {task_id} não encontrada.')

if __name__ == '__main__':
    task_manager = TaskManager()

    while True:
        print("1. Adicionar Tarefas")
        print("2. Listar Tarefas")
        print("3. Remover Tarefas")
        print("4. Sair")
        
        opcao = input("Informe sua escolha: ")
        if opcao == '1':
            description = input("Descreva a tarefa: ")
            task_manager.add_task(description)
        elif opcao == '2':
            task_manager.listar_tarefas()
        elif opcao == '3':
            task_id = input("Informe o ID da tarefa para ser removida: ")
            task_manager.remove_tarefa(task_id)
        elif opcao == '4':
            print("Saido...")
            print("Bye")
            break
        else:
            print("Escolha invlida.Escolha uma opcao valida.")