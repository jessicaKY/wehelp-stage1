// Assignment - Week 3 JavaScript

// ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
// Task 3
// Parse attraction data from internet and render first 3 bars + first 10 cards
// (從網路抓取景點資料，呈現前 3 個 bars 和前 10 個 cards)
// ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

const burgerButton = document.querySelector(".burger-button");                 // 取得手機版漢堡選單按鈕
const closeButton = document.querySelector(".close-button");                   // 取得手機版關閉選單按鈕
const mobileMenu = document.querySelector(".mobile-menu");                     // 取得手機版側邊選單
const menuBackdrop = document.querySelector(".menu-backdrop");                 // 取得選單開啟時的半透明背景
const barsContainer = document.querySelector(".bars");                         // 取得上方 3 個 promotion bars 的容器
const cardsContainer = document.querySelector(".cards");                       // 取得下方 content blocks 的容器

const DATA_URL = "https://cwpeng.github.io/test/assignment-3-1";               // 景點基本資料網址
const IMAGE_URL = "https://cwpeng.github.io/test/assignment-3-2";              // 景點圖片資料網址

let attractions = [];                                                          // 儲存合併完成的景點資料


function openMenu() {                                                          // 定義開啟手機選單函式
  mobileMenu.classList.add("open");                                            // 在側邊選單加上 open class
  mobileMenu.setAttribute("aria-hidden", "false");                             // 告訴輔助工具選單目前可見
  burgerButton.setAttribute("aria-expanded", "true");                          // 告訴輔助工具漢堡按鈕目前已展開
  menuBackdrop.hidden = false;                                                  // 顯示半透明背景
}                                                                              // openMenu 函式結束


function closeMenu() {                                                         // 定義關閉手機選單函式
  mobileMenu.classList.remove("open");                                         // 移除側邊選單的 open class
  mobileMenu.setAttribute("aria-hidden", "true");                              // 告訴輔助工具選單目前隱藏
  burgerButton.setAttribute("aria-expanded", "false");                         // 告訴輔助工具漢堡按鈕目前未展開
  menuBackdrop.hidden = true;                                                   // 隱藏半透明背景
}                                                                              // closeMenu 函式結束


function getFirstImageUrl(pictures, host) {                                    // 定義取得第一張圖片完整網址的函式
  if (!pictures) {                                                             // 如果圖片字串不存在
    return "";                                                                 // 回傳空字串，避免後面組網址出錯
  }                                                                            // if 判斷結束

  const firstPath = pictures.split(".jpg")[0] + ".jpg";                        // 用第一個 .jpg 切出第一張圖片路徑
  return host + firstPath;                                                     // 將 host 和圖片路徑組成完整圖片網址
}                                                                              // getFirstImageUrl 函式結束


function createBar(attraction, index) {                                        // 定義建立 promotion bar 的函式
  const bar = document.createElement("article");                               // 建立 article 元素當作 bar
  bar.className = "bar";                                                       // 加上 bar class 套用樣式

  if (index === 0) {                                                           // 如果是第一個 bar
    bar.classList.add("bar-large");                                            // 加上 bar-large class，符合 Week 1 版型
  }                                                                            // 第一個 bar 判斷結束

  if (index === 1) {                                                           // 如果是第二個 bar
    bar.classList.add("bar-wide");                                             // 加上 bar-wide class，符合 Week 1 版型
  }                                                                            // 第二個 bar 判斷結束

  const image = document.createElement("img");                                 // 建立圖片元素
  image.src = attraction.image;                                                // 設定圖片來源為景點第一張圖片
  image.alt = attraction.name;                                                 // 設定圖片替代文字為景點名稱

  const title = document.createElement("p");                                   // 建立文字段落元素
  title.textContent = attraction.name;                                         // 將景點名稱放入段落

  bar.appendChild(image);                                                      // 把圖片加入 bar
  bar.appendChild(title);                                                      // 把景點名稱加入 bar

  return bar;                                                                  // 回傳完成的 bar 元素
}                                                                              // createBar 函式結束


function createCard(attraction) {                                              // 定義建立 content block 卡片的函式
  const card = document.createElement("article");                              // 建立 article 元素當作卡片
  card.className = "card";                                                     // 加上 card class 套用樣式
  card.style.backgroundImage = `url("${attraction.image}")`;                   // 設定卡片背景圖為景點第一張圖片

  const star = document.createElement("button");                               // 建立星號按鈕
  star.className = "star";                                                     // 加上 star class 套用樣式
  star.type = "button";                                                        // 設定按鈕型態，避免預設 submit 行為
  star.setAttribute("aria-label", `Favorite ${attraction.name}`);              // 設定輔助工具可讀的按鈕名稱
  star.textContent = "★";                                                      // 顯示星號文字

  const title = document.createElement("p");                                   // 建立卡片標題段落
  title.textContent = attraction.name;                                         // 將景點名稱放入卡片標題

  card.appendChild(star);                                                      // 把星號按鈕加入卡片
  card.appendChild(title);                                                     // 把景點名稱加入卡片

  return card;                                                                 // 回傳完成的卡片元素
}                                                                              // createCard 函式結束


function renderBars() {                                                        // 定義呈現上方 3 個 bars 的函式
  barsContainer.textContent = "";                                              // 先清空 bars 容器，避免重複呈現

  attractions.slice(0, 3).forEach((attraction, index) => {                     // 只取前 3 筆景點資料
    barsContainer.appendChild(createBar(attraction, index));                   // 建立 bar 並加入 bars 容器
  });                                                                          // forEach 迴圈結束
}                                                                              // renderBars 函式結束


function renderInitialCards() {                                                // 定義第一次呈現 10 個 content blocks 的函式
  cardsContainer.textContent = "";                                             // 先清空 cards 容器，避免重複呈現

  attractions.slice(3, 13).forEach((attraction) => {                            // 取第 4 筆到第 13 筆，共 10 筆資料
    cardsContainer.appendChild(createCard(attraction));                         // 建立卡片並加入 cards 容器
  });                                                                          // forEach 迴圈結束
}                                                                              // renderInitialCards 函式結束


async function loadAttractions() {                                             // 主函式：Task 3
  const [dataResponse, imageResponse] = await Promise.all([                    // 同時下載基本資料與圖片資料
    fetch(DATA_URL),                                                           // 下載景點基本資料
    fetch(IMAGE_URL),                                                          // 下載景點圖片資料
  ]);                                                                          // Promise.all 結束

  const dataJson = await dataResponse.json();                                  // 將景點基本資料轉成 JSON 物件
  const imageJson = await imageResponse.json();                                // 將景點圖片資料轉成 JSON 物件

  const imageBySerial = {};                                                    // 建立用 serial 查圖片網址的物件

  imageJson.rows.forEach((item) => {                                           // 逐一讀取圖片資料
    imageBySerial[item.serial] = getFirstImageUrl(item.pics, imageJson.host);  // 用 serial 存入第一張圖片完整網址
  });                                                                          // 圖片資料 forEach 結束

  attractions = dataJson.rows                                                  // 從景點基本資料開始轉換
    .map((item) => ({                                                          // 將每筆資料整理成畫面需要的格式
      name: item.sname,                                                        // 景點名稱
      image: imageBySerial[item.serial],                                       // 用 serial 找到對應圖片
    }))                                                                        // map 結束
    .filter((item) => item.image);                                             // 只保留有圖片的景點資料

  renderBars();                                                                // 呈現前 3 筆到 bars
  renderInitialCards();                                                        // 呈現接下來 10 筆到 content blocks
  updateLoadMoreButton();                                                      // 檢查是否還有下一批資料，沒有就隱藏按鈕
}                                                                              // loadAttractions 函式結束


burgerButton.addEventListener("click", openMenu);                              // 點擊漢堡按鈕時開啟手機選單
closeButton.addEventListener("click", closeMenu);                              // 點擊關閉按鈕時關閉手機選單
menuBackdrop.addEventListener("click", closeMenu);                             // 點擊背景時關閉手機選單

window.addEventListener("keydown", (event) => {                                // 監聽鍵盤按鍵事件
  if (event.key === "Escape") {                                                // 如果按下 Escape 鍵
    closeMenu();                                                               // 關閉手機選單
  }                                                                            // if 判斷結束
});                                                                            // keydown 事件監聽結束

window.addEventListener("load", loadAttractions);                              // 頁面載入完成後開始下載並呈現景點資料



// ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
// Task 4
// Build paging mechanism by Load More button
// (建立 Load More 按鈕，每次點擊後再載入下一批 10 個景點)
// ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

const loadMoreButton = document.querySelector(".load-more-button");            // 取得 Load More 按鈕
const PAGE_SIZE = 10;                                                          // 每次顯示 10 個 content blocks

let nextCardIndex = 13;                                                        // Task 3 已經顯示前 13 筆，下一批從第 14 筆開始


function updateLoadMoreButton() {                                              // 定義更新 Load More 按鈕顯示狀態的函式
  loadMoreButton.hidden = nextCardIndex >= attractions.length;                 // 如果資料已全部顯示，就隱藏 Load More 按鈕
}                                                                              // updateLoadMoreButton 函式結束


function renderNextCards() {                                                   // 主函式：Task 4
  const endIndex = Math.min(nextCardIndex + PAGE_SIZE, attractions.length);    // 計算這次最多呈現到哪一筆，不能超過資料總數

  for (let i = nextCardIndex; i < endIndex; i += 1) {                          // 從目前索引開始逐筆呈現
    cardsContainer.appendChild(createCard(attractions[i]));                    // 建立卡片並加入 cards 容器
  }                                                                            // for 迴圈結束

  nextCardIndex = endIndex;                                                    // 更新下一次開始呈現的位置
  updateLoadMoreButton();                                                      // 檢查是否還有下一批資料，沒有就隱藏按鈕
}                                                                              // renderNextCards 函式結束


loadMoreButton.addEventListener("click", renderNextCards);                     // 點擊 Load More 時載入下一批卡片
