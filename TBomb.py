import os
import random
import concurrent.futures

def create_random_file(folder_name, file_size):
    file_name = f"file_{random.randint(0, 100000)}.txt"
    file_path = os.path.join(folder_name, file_name)
    random_number = random.randint(0, 100000)
    words = "balls"
    random_index = random.randint(0, len(words) - 1)
    random_word = words[random_index]

    content = f"Random number: {random_number}\r\nRandom word: {random_word}\n"
    content_size = len(content.encode('utf-8'))

    with open(file_path, 'w') as f:
        f.write(content)

    if file_size > content_size:
        write_additional_content(file_path, random_word, file_size - content_size)

def write_additional_content(file_path, word, size):
    with open(file_path, 'ab') as f:
        chunk_size = 16384 * 16384
        chunk = (word * chunk_size).encode('utf-8')
        while size > 0:
            write_size = min(chunk_size, size)
            f.write(chunk[:write_size])
            size -= write_size

def main():
    num_files = int(input("Enter the number of files to create: "))
    folder_name = "TBomb"
    file_size = int(input("Desired file size in bytes: "))

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    max_workers = min(num_files, os.cpu_count() * 20)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(create_random_file, folder_name, file_size) for _ in range(num_files)]
        for future in concurrent.futures.as_completed(futures):
            future.result()

    print("Folder and files created successfully.")

if __name__ == "__main__":
    main()