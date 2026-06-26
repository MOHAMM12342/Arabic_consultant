package baddi.arabic_nlp.Controller;

import baddi.arabic_nlp.Services.OrchestratorService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

import java.util.Map;

@RestController
@RequestMapping("/api/chat")
@CrossOrigin(origins = "*")
public class ChatController {

    @Autowired
    private OrchestratorService orchestratorService;

    @PostMapping
    public Mono<Map<String, String>> chat(@RequestBody Map<String, String> request) {
        String query = request.get("query");
        if (query == null || query.trim().isEmpty()) {
            return Mono.just(Map.of("error", "Query must not be empty"));
        }
        
        return orchestratorService.processDarijaQuery(query)
                .map(response -> Map.of("response", response))
                .onErrorResume(e -> Mono.just(Map.of("error", "An error occurred: " + e.getMessage())));
    }
}
