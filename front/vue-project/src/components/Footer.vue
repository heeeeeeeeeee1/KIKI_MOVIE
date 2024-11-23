<template>
  <footer class="footer">
    <div class="footer-content">
      <section class="footer-section service-info">
        <h4>키키 무비</h4>
        <p>© 2024 키키무비(Kiki movie). All Rights Reserved.</p>
      </section>
      <div class="footer-subcontent">
        <section class="footer-section links">
          <h4>메뉴</h4>
          <ul>
            <li><a href="javascript:void(0)">이용약관</a></li>
            <li><a href="javascript:void(0)">개인정보 처리방침</a></li>
            <li><a href="javascript:void(0)">고객 지원</a></li>
          </ul>
        </section>
        <section class="footer-section social-media">
          <h4>개발자</h4>
          <ul class="icons">
            <li><a href="https://github.com/heeeeeeeeeee1/BAKI_MINGKI">키키무비</a></li>
            <li><a href="https://github.com/heeeeeeeeeee1">바키</a></li>
            <li><a href="https://github.com/minjeeki">밍키</a></li>
          </ul>
        </section>
      </div>
    </div>
  </footer>
</template>

<script setup>
  // 필요한 추가 로직이 있다면 여기 작성
</script>

<style scoped>
.footer {
  background-color: black;
  color: white;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.footer-content {
  width: 70%;
  display: flex;
  flex-direction: column;
  align-items: space-around;
}
.footer-subcontent {
  display: flex;
  justify-content: space-between;
}
.footer-section {
  display: flex;
  align-items: center;
}
.footer-section:first-child {
  margin-bottom: 0.5rem;
}
.footer-section h4 {
  margin-right: 1rem;
}

.footer-section p {
  font-size: 0.8rem;
}

.footer-section div {
  display: flex;
}
.footer-section ul {
  display: flex;
  list-style: none;
  padding: 0;
}

.footer-section ul li {
  margin: 5px 0;
  font-size: 0.8rem;
}
.footer-section ul li:not(:last-child) {
  margin-right: 0.5rem;
}
.footer-section a {
  color: #fff;
  text-decoration: none;
}

.footer-section a:hover {
  text-decoration: underline;
}
</style>
