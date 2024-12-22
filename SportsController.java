package com.example.sports;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.Map;

@Controller
public class SportsController {

    private static final String API_URL = "https://v3.football.api-sports.io/fixtures?live=all";
    private static final String API_KEY = "24fcd56d1900ce220d7906f9f2a9ed87";

    @GetMapping("/")
    public String getLiveMatches(Model model) {
        // API 호출
        RestTemplate restTemplate = new RestTemplate();
        String response = restTemplate.getForObject(API_URL + "&x-apisports-key=" + API_KEY, String.class);

        // JSON 파싱
        // 결과 데이터를 파싱하여 model에 전달
        model.addAttribute("matches", parseMatches(response));

        return "index";  // Thymeleaf 템플릿 이름
    }

    private List<Map<String, Object>> parseMatches(String response) {
        // API 응답을 JSON에서 필요한 데이터로 변환
        // 실제로는 JSON 파싱 라이브러리 (예: Jackson)를 사용하여 JSON을 객체로 변환해야 함
        // 여기서는 응답 데이터를 처리하는 방법을 예시로 보여줍니다
        return null;  // 실제 파싱 코드 작성
    }
}
