import heapq

# ------------------------
# 휴리스틱: 맨해튼 거리
# ------------------------
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# ------------------------
# 이웃 (상하좌우)
# ------------------------
def get_neighbors(grid, node):
    x, y = node
    for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            if grid[nx][ny] == 0:  # 0이면 통과 가능
                yield (nx, ny)

# ------------------------
# A* 알고리즘
# ------------------------
def a_star(grid, start, goal):
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))
    came_from = {}
    g_score = {start: 0}
    visited = set()

    while open_set:
        f, curg, current = heapq.heappop(open_set)
        if current == goal:
            # 경로 복원
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return list(reversed(path)), g_score, visited

        visited.add(current)

        for nb in get_neighbors(grid, current):
            tentative_g = curg + 1
            if nb not in g_score or tentative_g < g_score[nb]:
                g_score[nb] = tentative_g
                fscore = tentative_g + heuristic(nb, goal)
                heapq.heappush(open_set, (fscore, tentative_g, nb))
                came_from[nb] = current

    return None, g_score, visited

# ------------------------
# 콘솔에 미로 출력 (문자)
# ------------------------
def print_maze(grid, start, goal, path=None):
    rows = len(grid)
    cols = len(grid[0])
    path_set = set(path) if path else set()
    for i in range(rows):
        line = []
        for j in range(cols):
            if (i, j) == start:
                line.append('S')
            elif (i, j) == goal:
                line.append('G')
            elif grid[i][j] == 1:
                line.append('#')
            elif (i, j) in path_set:
                line.append('*')
            else:
                line.append('.')
        print(''.join(line))
    print()

# ------------------------
# 콘솔에 휴리스틱(h)값 출력
# ------------------------
def print_heuristic_grid(grid, goal):
    rows = len(grid)
    cols = len(grid[0])
    print("Heuristic h(x) (맨해튼 거리 to goal) :")
    for i in range(rows):
        row_vals = []
        for j in range(cols):
            if grid[i][j] == 1:
                row_vals.append(" --")   # 벽
            else:
                h = heuristic((i,j), goal)
                row_vals.append(f"{h:3d}")
        print(' '.join(row_vals))
    print()

# ------------------------
# 예제 미로 정의 (0=통로, 1=벽)
# ------------------------
def make_sample_grid():
    rows, cols = 10, 10
    grid = [[0]*cols for _ in range(rows)]
    # 벽 추가 (예시)
    for j in range(1,8):
        grid[3][j] = 1
    for j in range(2,9):
        grid[6][j] = 1
    # 테두리 벽도 원하면 추가 가능 (현재는 내부 장애물만)
    return grid

# ------------------------
# main
# ------------------------
if __name__ == "__main__":
    grid = make_sample_grid()
    start = (0, 0)
    goal  = (9, 9)

    print("Maze:")
    print_maze(grid, start, goal)

    print_heuristic_grid(grid, goal)

    path, g_scores, visited = a_star(grid, start, goal)
    if path:
        print("A*가 찾은 최단 경로 (S=start, G=goal, *=경로, #=벽):")
        print_maze(grid, start, goal, path)
        print("경로 좌표 (시작 -> 목표):")
        print(path)
        print(f"경로 길이: {len(path)-1} (이동 횟수)")
    else:
        print("경로를 찾지 못했습니다.")
