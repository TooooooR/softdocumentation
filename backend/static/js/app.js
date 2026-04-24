const PAGE_SIZE = 100;

const state = {
    posts: [],
    editId: null,
    offset: 0,
    totalPosts: 0,
};

const bodyEl = document.getElementById("posts-body");
const modalBackdrop = document.getElementById("modal-backdrop");
const formEl = document.getElementById("post-form");
const modalTitleEl = document.getElementById("modal-title");
const prevPageEl = document.getElementById("prev-page");
const nextPageEl = document.getElementById("next-page");
const pageCurrentEl = document.getElementById("page-current");
const pageMetaEl = document.getElementById("page-meta");

function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}

function renderRows() {
    if (!state.posts.length) {
        bodyEl.innerHTML = '<tr><td colspan="7" class="muted">Записів не знайдено. Додайте перший допис.</td></tr>';
        return;
    }

    bodyEl.innerHTML = state.posts
        .map(
            (post) => `
                <tr>
                    <td>${post.id}</td>
                    <td>${escapeHtml(post.post_title)}</td>
                    <td>${escapeHtml(post.post_content)}</td>
                    <td>${escapeHtml(post.post_tag)}</td>
                    <td>${escapeHtml(post.username)}</td>
                    <td>${escapeHtml(post.email)}</td>
                    <td>
                        <div class="actions">
                            <button class="btn btn-light" data-action="edit" data-id="${post.id}">Редагувати</button>
                            <button class="btn btn-danger" data-action="delete" data-id="${post.id}">Видалити</button>
                        </div>
                    </td>
                </tr>
            `
        )
        .join("");
}

async function loadPosts() {
    const [postsResponse, statsResponse] = await Promise.all([
        fetch(`/posts?limit=${PAGE_SIZE}&offset=${state.offset}`),
        fetch("/stats"),
    ]);

    if (!postsResponse.ok || !statsResponse.ok) {
        alert("Помилка завантаження списку дописів");
        return;
    }

    state.posts = await postsResponse.json();
    const stats = await statsResponse.json();
    state.totalPosts = Number(stats.total_posts ?? 0);

    if (state.offset >= state.totalPosts && state.offset > 0) {
        state.offset = Math.max(0, state.offset - PAGE_SIZE);
        await loadPosts();
        return;
    }

    renderRows();
    renderPagination();
}

function renderPagination() {
    const totalPages = Math.max(1, Math.ceil(state.totalPosts / PAGE_SIZE));
    const currentPage = Math.floor(state.offset / PAGE_SIZE) + 1;
    const start = state.totalPosts === 0 ? 0 : state.offset + 1;
    const end = state.offset + state.posts.length;

    pageCurrentEl.textContent = `Сторінка ${currentPage} з ${totalPages}`;
    pageMetaEl.textContent = `Показано ${start}-${end} з ${state.totalPosts}`;

    prevPageEl.disabled = state.offset === 0;
    nextPageEl.disabled = state.offset + PAGE_SIZE >= state.totalPosts;
}

function openModal(post = null) {
    state.editId = post ? post.id : null;
    modalTitleEl.textContent = post ? "Редагувати допис" : "Додати допис";
    formEl.username.value = post?.username ?? "";
    formEl.email.value = post?.email ?? "";
    formEl.post_title.value = post?.post_title ?? "";
    formEl.post_tag.value = post?.post_tag ?? "";
    formEl.post_content.value = post?.post_content ?? "";
    modalBackdrop.style.display = "flex";
}

function closeModal() {
    modalBackdrop.style.display = "none";
    state.editId = null;
    formEl.reset();
}

async function savePost(event) {
    event.preventDefault();
    const payload = {
        username: formEl.username.value,
        email: formEl.email.value,
        post_title: formEl.post_title.value,
        post_tag: formEl.post_tag.value,
        post_content: formEl.post_content.value,
    };

    const isEdit = state.editId !== null;
    const url = isEdit ? `/posts/${state.editId}` : "/posts";
    const method = isEdit ? "PUT" : "POST";

    const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        const err = await response.json().catch(() => ({ detail: "Невідома помилка" }));
        alert(`Помилка: ${err.detail ?? "Невідома помилка"}`);
        return;
    }

    closeModal();
    await loadPosts();
}

async function removePost(postId) {
    const confirmed = confirm(`Видалити допис #${postId}?`);
    if (!confirmed) {
        return;
    }

    const response = await fetch(`/posts/${postId}`, { method: "DELETE" });
    if (!response.ok) {
        alert("Не вдалося видалити допис");
        return;
    }

    await loadPosts();
}

document.getElementById("add-btn").addEventListener("click", () => openModal());
document.getElementById("cancel-btn").addEventListener("click", closeModal);
formEl.addEventListener("submit", savePost);
prevPageEl.addEventListener("click", async () => {
    if (state.offset === 0) {
        return;
    }

    state.offset = Math.max(0, state.offset - PAGE_SIZE);
    await loadPosts();
});

nextPageEl.addEventListener("click", async () => {
    if (state.offset + PAGE_SIZE >= state.totalPosts) {
        return;
    }

    state.offset += PAGE_SIZE;
    await loadPosts();
});

bodyEl.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLElement)) {
        return;
    }

    const action = target.dataset.action;
    const idRaw = target.dataset.id;
    if (!action || !idRaw) {
        return;
    }

    const postId = Number(idRaw);
    if (!Number.isFinite(postId)) {
        return;
    }

    if (action === "edit") {
        const post = state.posts.find((item) => item.id === postId);
        if (post) {
            openModal(post);
        }
    }

    if (action === "delete") {
        removePost(postId);
    }
});

modalBackdrop.addEventListener("click", (event) => {
    if (event.target === modalBackdrop) {
        closeModal();
    }
});

loadPosts();
