import asyncio

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class AsyncCircularLinkedList:
    def __init__(self):
        self.head = None
        self.current = None
        self.lock = asyncio.Lock()
        self.node_count = 0

    async def append(self, data):
        async with self.lock:
            new_node = Node(data)
            if not self.head:
                self.head = new_node
                new_node.next = self.head
                self.current = self.head

            else:
                last_node = self.head
                while last_node.next != self.head:
                    last_node = last_node.next
                last_node.next = new_node
                new_node.next = self.head
            self.node_count += 1

    async def traverse(self, num_elements=None):
        async with self.lock:
            current_node = self.head
            count = 0
            while current_node and (num_elements is None or count < num_elements):
                print(current_node.data)
                current_node = current_node.next
                count += 1
                if current_node == self.head:
                    break

    async def traverse_from_current(self, num_elements=None):
        async with self.lock:
            count = 0
            current_node = self.current
            while current_node and (num_elements is None or count < num_elements):
                print(current_node.data)
                current_node = current_node.next
                count += 1
                if current_node == self.head:
                    break
            self.current = current_node

    async def get_node_count(self):
        async with self.lock:
            return self.node_count

async def main():
    ll = AsyncCircularLinkedList()
    await ll.append(1)
    await ll.append(2)
    await ll.append(3)
    await ll.traverse(10)

    node_count = await ll.get_node_count()
    print(f"Node count: {node_count}")

# asyncio.run(main())
