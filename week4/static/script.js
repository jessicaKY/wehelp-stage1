// Assignment - Week 4 JavaScript

const loginForm = document.querySelector("#login-form");               // 取得首頁登入表單，後面用來監聽 submit 事件
const agreementCheckbox = document.querySelector("#agreement");        // 取得同意條款 checkbox，後面用來檢查是否有勾選
const hotelForm = document.querySelector("#hotel-form");               // 取得旅館查詢表單，後面用來監聽 submit 事件
const hotelIdInput = document.querySelector("#hotel-id");              // 取得旅館編號輸入框，後面用來讀取使用者輸入的 ID


loginForm.addEventListener("submit", (event) => {                      // Task 1 Home Page：處理登入表單送出前的 checkbox 檢查
  if (!agreementCheckbox.checked) {                                     // 如果同意條款 checkbox 沒有被勾選
    event.preventDefault();                                             // 阻止登入表單送到後端 /login
    alert("請勾選同意條款");                                             // 顯示 PDF 要求的提示訊息
  }                                                                     // checkbox 檢查結束
});                                                                    // 登入表單 submit 事件監聽結束


hotelForm.addEventListener("submit", (event) => {                      // Task 4 Path Parameter：處理旅館查詢表單送出前的正整數檢查
  event.preventDefault();                                               // 阻止表單預設送出，改由 JavaScript 控制導頁

  const hotelId = hotelIdInput.value.trim();                            // 取得旅館編號輸入值，並移除前後空白
  const positiveIntegerPattern = /^[1-9]\d*$/;                          // 建立正整數規則，第一位必須是 1 到 9

  if (!positiveIntegerPattern.test(hotelId)) {                          // 如果輸入值不符合正整數規則
    alert("請輸入正整數");                                               // 顯示要求的提示訊息
    return;                                                             // 結束函式，不繼續導向旅館頁
  }                                                                     // 正整數檢查結束

  window.location.href = `/hotel/${hotelId}`;                           // 導向 FastAPI 的 /hotel/{hotel_id} 路由
});                                                                    // 旅館查詢表單 submit 事件監聽結束
