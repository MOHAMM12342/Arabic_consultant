package baddi.arabic_nlp.Services;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

@Component
public class LegalModelClient {
    private final WebClient webClient;

    public LegalModelClient(WebClient.Builder builder) {
        this.webClient = builder.baseUrl("http://python-legal-model:8001").build();
    }

    public String getLegalResponse(String augmentedPrompt) {
        // Connexion au Modèle juridique en Arabe classique
        return webClient.post()
                .uri("/generate/legal-advice")
                .bodyValue(augmentedPrompt)
                .retrieve()
                .bodyToMono(String.class)
                .block();
    }
}