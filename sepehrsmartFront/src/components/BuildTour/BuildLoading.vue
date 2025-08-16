<template>
  <div class="loading-container">
    <div class="loading-content">
      <div class="loading-scene">
        <!-- Hotel Building -->
        <div class="hotel">
          <div class="hotel-body">
            <div class="windows-row">
              <div class="window"></div>
              <div class="window"></div>
              <div class="window"></div>
            </div>
            <div class="windows-row">
              <div class="window"></div>
              <div class="window"></div>
              <div class="window"></div>
            </div>
            <div class="entrance">
              <div class="door"></div>
              <div class="steps"></div>
            </div>
          </div>
          <div class="hotel-roof">
            <div class="hotel-sign">HOTEL</div>
          </div>
        </div>

        <!-- Data Streams -->
        <div class="data-streams">
          <div class="stream-container">
            <div class="stream stream-1">
              <span class="site-icon">✈️</span>
              <span class="site-name">MehrabSeir</span>
            </div>
            <div class="stream stream-2">
              <span class="site-icon">🏨</span>
              <span class="site-name">Eram2MHD</span>
            </div>
            <div class="stream stream-3">
              <span class="site-icon">✈️</span>
              <span class="site-name">HRC</span>
            </div>
            <div class="stream stream-4">
              <span class="site-icon">🏨</span>
              <span class="site-name">Kimiya</span>
            </div>
            <div class="stream stream-5">
              <span class="site-icon">✈️</span>
              <span class="site-name">TakSefareh</span>
            </div>
            <div class="stream stream-6">
              <span class="site-icon">🏨</span>
              <span class="site-name">Parmis</span>
            </div>
            <div class="stream stream-7">
              <span class="site-icon">✈️</span>
              <span class="site-name">Rahbal</span>
            </div>
            <div class="stream stream-8">
              <span class="site-icon">🏨</span>
              <span class="site-name">Safiran</span>
            </div>
            <div class="stream stream-9">
              <span class="site-icon">✈️</span>
              <span class="site-name">OmidOj</span>
            </div>
            <div class="stream stream-10">
              <span class="site-icon">🏨</span>
              <span class="site-name">SepidParvaz</span>
            </div>
            <div class="stream stream-11">
              <span class="site-icon">✈️</span>
              <span class="site-name">Hamood</span>
            </div>
            <div class="stream stream-12">
              <span class="site-icon">🏨</span>
              <span class="site-name">DayanSafar</span>
            </div>
            <div class="stream stream-13">
              <span class="site-icon">✈️</span>
              <span class="site-name">Darvishi</span>
            </div>
            <div class="stream stream-14">
              <span class="site-icon">🏨</span>
              <span class="site-name">MoeinDarbari</span>
            </div>
            <div class="stream stream-15">
              <span class="site-icon">✈️</span>
              <span class="site-name">Deltaban</span>
            </div>
            <div class="stream stream-16">
              <span class="site-icon">🏨</span>
              <span class="site-name">Jimboo</span>
            </div>
            <div class="stream stream-17">
              <span class="site-icon">✈️</span>
              <span class="site-name">Booking</span>
            </div>
            <div class="stream stream-18">
              <span class="site-icon">🏨</span>
              <span class="site-name">SnappTrip</span>
            </div>
            <div class="stream stream-19">
              <span class="site-icon">✈️</span>
              <span class="site-name">Alaedin</span>
            </div>
            <div class="stream stream-20">
              <span class="site-icon">🏨</span>
              <span class="site-name">Alibaba</span>
            </div>
            <div class="stream stream-21">
              <span class="site-icon">✈️</span>
              <span class="site-name">Alwin24</span>
            </div>
          </div>
        </div>
      </div>

      <h3 class="loading-text">در حال ساخت تور اختصاصی شما</h3>
      <p class="loading-subtext">جستجو در سایت‌های معتبر رزرواسیون</p>
      
      <div class="loading-dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "BuildLoading"
}
</script>

<style scoped>
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
  width: 100%;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.loading-content {
  text-align: center;
  width: 100%;
  padding: 20px;
}

.loading-scene {
  position: relative;
  height: 160px;
  margin: 0 auto 30px;
  width: 800px;
}

/* Hotel Styles */
.hotel {
  position: absolute;
  bottom: 30px;
  left: 40px;
  width: 120px;
  height: 120px;
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
  z-index: 2;
}

.hotel-body {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 90px;
  background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  padding: 8px;
  gap: 4px;
}

.windows-row {
  display: flex;
  justify-content: space-around;
  margin-bottom: 4px;
}

.window {
  width: 20px;
  height: 20px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 4px;
  box-shadow: inset 0 0 4px rgba(0,0,0,0.1);
}

.entrance {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.door {
  width: 30px;
  height: 35px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 4px 4px 0 0;
  box-shadow: inset 0 0 4px rgba(0,0,0,0.1);
}

.steps {
  width: 40px;
  height: 6px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 2px;
}

.hotel-roof {
  position: absolute;
  top: -25px;
  width: 140%;
  height: 35px;
  background: linear-gradient(135deg, #1976D2 0%, #0D47A1 100%);
  left: -20%;
  clip-path: polygon(50% 0%, 100% 100%, 0% 100%);
  display: flex;
  justify-content: center;
  align-items: center;
}

.hotel-sign {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.6rem;
  font-weight: bold;
  transform: translateY(8px);
}

/* Data Streams */
.data-streams {
  position: absolute;
  top: 0;
  right: -180px;
  height: 160px;
  width: 400px;
  display: flex;
  justify-content: flex-end;
}

.stream-container {
  display: grid;
  grid-template-columns: repeat(3, minmax(120px, 1fr));
  gap: 6px;
  padding: 5px;
  height: 100%;
  overflow-y: auto;
  scrollbar-width: none;
}

.stream-container::-webkit-scrollbar {
  display: none;
}

.stream {
  position: relative;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  background: rgba(255, 255, 255, 0.98);
  border: 1px solid rgba(33, 150, 243, 0.3);
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(33, 150, 243, 0.15);
  opacity: 0;
  transform: scale(0.9);
  animation: streamCycle 8s infinite;
  height: 28px;
  z-index: 10;
}

.site-icon {
  font-size: 0.9rem;
  flex-shrink: 0;
}

.site-name {
  font-size: 0.8rem;
  color: #1976D2;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Generate stream delays */
.stream-1 { animation-delay: 0.0s; }
.stream-2 { animation-delay: 0.2s; }
.stream-3 { animation-delay: 0.4s; }
.stream-4 { animation-delay: 0.6s; }
.stream-5 { animation-delay: 0.8s; }
.stream-6 { animation-delay: 1.0s; }
.stream-7 { animation-delay: 1.2s; }
.stream-8 { animation-delay: 1.4s; }
.stream-9 { animation-delay: 1.6s; }
.stream-10 { animation-delay: 1.8s; }
.stream-11 { animation-delay: 2.0s; }
.stream-12 { animation-delay: 2.2s; }
.stream-13 { animation-delay: 2.4s; }
.stream-14 { animation-delay: 2.6s; }
.stream-15 { animation-delay: 2.8s; }
.stream-16 { animation-delay: 3.0s; }
.stream-17 { animation-delay: 3.2s; }
.stream-18 { animation-delay: 3.4s; }
.stream-19 { animation-delay: 3.6s; }
.stream-20 { animation-delay: 3.8s; }
.stream-21 { animation-delay: 4.0s; }

@keyframes streamCycle {
  0% {
    opacity: 0;
    transform: scale(0.9) translateX(20px);
  }
  5% {
    opacity: 1;
    transform: scale(1) translateX(0);
  }
  45% {
    opacity: 1;
    transform: scale(1) translateX(0);
  }
  50% {
    opacity: 0;
    transform: scale(0.9) translateX(-20px);
  }
  100% {
    opacity: 0;
    transform: scale(0.9) translateX(-20px);
  }
}

/* Remove all other icon styles */
.airplane, 
.package, 
.airplane-trail {
  display: none;
}

/* Keep only necessary animations */
@keyframes dots {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(0.5);
    opacity: 0.5;
  }
}

.loading-text {
  color: #333;
  font-size: 1.2rem;
  margin-bottom: 8px;
}

.loading-subtext {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 15px;
}

.loading-dots {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.loading-dots span {
  width: 8px;
  height: 8px;
  background-color: #2196F3;
  border-radius: 50%;
  animation: dots 1.4s infinite;
}

.loading-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.loading-dots span:nth-child(3) {
  animation-delay: 0.4s;
}
</style>