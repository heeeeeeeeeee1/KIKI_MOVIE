export const actorMappings = {
  강동원: 83014, // TMDB ID
  강소라: 1295457, // TMDB ID
  강하늘: 488623, // TMDB ID
  고아성: 21689, // TMDB ID
  고현정: 1245069, // TMDB ID
  공효진: 126881, // TMDB ID
  김고은: 1067849, // TMDB ID
  김남길: 110388, // TMDB ID
  김민희: 123664, // TMDB ID
  김수현: 1251581, // TMDB ID
  김태리: 1537768, // TMDB ID
  김혜수: 146245, // TMDB ID
  남주혁: 1459772, // TMDB ID
  류준열: 1530733, // TMDB ID
  마동석: 1024395,
  박보영: 83036, // TMDB ID
  박서준: 1347525, // TMDB ID
  박신혜: 1156197, // TMDB ID
  박해일: 21687, // TMDB ID
  배두나: 21688, // TMDB ID
  배수지: 1014784,
  변요한: 1337780, // TMDB ID
  손예진: 86889, // TMDB ID
  송강호: 20738, // TMDB ID
  송중기: 150698, // TMDB ID
  신민아: 116175, // TMDB ID
  안성기: 17121, // TMDB ID
  유아인: 572225, // TMDB ID
  유연석: 587675, // TMDB ID
  이병헌: 25002,
  이정재: 73249, // TMDB ID
  이종석: 1095818, // TMDB ID
  이주연: 832881, // TMDB ID
  임시완: 1296713, // TMDB ID
  전도연: 20737, // TMDB ID
  전지현: 63436, // TMDB ID
  정우성: 17120, // TMDB ID
  조인성: 127564, // TMDB ID
  주지훈: 150125, // TMDB ID
  지창욱: 1253391, // TMDB ID
  차승원: 1248450, // TMDB ID
  최민식: 64880, // TMDB ID
  한지민: 1010877, // TMDB ID
  한효주: 240145, // TMDB ID
  황정민: 68903, // TMDB ID
  현빈: 544107, // TMDB ID
  김윤석: 75912, // TMDB ID
  김희애: 1304595, // TMDB ID
  이성민: 141548, // TMDB ID
  조진웅: 138336, // TMDB ID
};

export function getActorId(actorName) {
  return actorMappings[actorName] || null;
}
