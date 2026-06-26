package baddi.arabic_nlp.Services;

import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class OrchestratorService {

    private final WebClient webClient;

    @Value("${service.translation.url:http://localhost:8002}")
    private String translationServiceUrl;

    @Value("${service.rag.url:http://localhost:8001}")
    private String ragServiceUrl;

    @Value("${service.llm.url:http://localhost:8003}")
    private String llmServiceUrl;

    public OrchestratorService(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder.build();
    }

    public Mono<String> processDarijaQuery(String darijaQuery) {
        // 1. Translate Darija to Arabic
        return webClient.post()
                .uri(translationServiceUrl + "/translate/dar-to-ar")
                .bodyValue(Map.of("text", darijaQuery))
                .retrieve()
                .bodyToMono(Map.class)
                .map(response -> (String) response.get("translated_text"))
                .flatMap(arabicQuery -> {
                    // 2. Retrieve Context from RAG
                    return webClient.post()
                            .uri(ragServiceUrl + "/retrieve")
                            .bodyValue(Map.of("query", arabicQuery, "top_k", 3))
                            .retrieve()
                            .bodyToMono(Map.class)
                            .flatMap(ragResponse -> {
                                List<Map<String, Object>> results = (List<Map<String, Object>>) ragResponse.get("results");
                                String context = results.stream()
                                        .map(res -> (String) res.get("content"))
                                        .collect(Collectors.joining("\n"));

                                // 3. Generate response using Consultant LLM
                                return webClient.post()
                                        .uri(llmServiceUrl + "/generate")
                                        .bodyValue(Map.of("query", arabicQuery, "context", context))
                                        .retrieve()
                                        .bodyToMono(Map.class)
                                        .map(llmResponse -> (String) llmResponse.get("response"));
                            });
                })
                .flatMap(arabicResponse -> {
                    // 4. Translate response back to Darija
                    return webClient.post()
                            .uri(translationServiceUrl + "/translate/ar-to-dar")
                            .bodyValue(Map.of("text", arabicResponse))
                            .retrieve()
                            .bodyToMono(Map.class)
                            .map(response -> (String) response.get("translated_text"));
                });
    }
}
