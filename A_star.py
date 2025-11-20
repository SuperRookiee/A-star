import heapq
import random

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
            if grid[nx][ny] == 0:
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
# 콘솔 출력 (문자)
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
# 휴리스틱 화면 출력
# ------------------------
def print_heuristic_grid(grid, goal):
    rows = len(grid)
    cols = len(grid[0])
    print("Heuristic h(x) (맨해튼 거리):")
    for i in range(rows):
        row_vals = []
        for j in range(cols):
            if grid[i][j] == 1:
                row_vals.append(" --")
            else:
                h = heuristic((i,j), goal)
                row_vals.append(f"{h:3d}")
        print(' '.join(row_vals))
    print()

# ------------------------
# 더 크고 복잡한 랜덤 미로 생성
# ------------------------
def make_random_grid(rows=30, cols=30, wall_ratio=0.25):
    grid = [[0]*cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if random.random() < wall_ratio:
                grid[i][j] = 1  # 벽

    # 시작과 끝은 반드시 통로
    grid[0][0] = 0
    grid[rows-1][cols-1] = 0
    return grid

# ------------------------
# main
# ------------------------
if __name__ == "__main__":
    grid = make_random_grid(30, 30, wall_ratio=0.25)
    start = (0, 0)
    goal  = (29, 29)

    print("Maze:")
    print_maze(grid, start, goal)

    print_heuristic_grid(grid, goal)

    path, g_scores, visited = a_star(grid, start, goal)
    if path:
        print("A* 최단 경로:")
        print_maze(grid, start, goal, path)
        print("경로 좌표:")
        print(path)
        print(f"경로 길이: {len(path)-1}")
    else:
        print("경로 없음 (막힌 미로일 수 있음)")
