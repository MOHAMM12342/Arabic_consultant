package baddi.arabic_nlp.Services;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

// Gère les services de traduction
@Component
public class TranslationClient {
    private final WebClient webClient;

    public TranslationClient(WebClient.Builder builder) {
        // L'URL pointe vers vos services Python
        this.webClient = builder.baseUrl("http://python-translation-service:8000").build();
    }

    public String translateDarijaToArabe(String text) {
        //  Appel au Model traducteur du darija en arabe
        return webClient.post()
                .uri("/translate/darija-to-arabe")
                .bodyValue(text)
                .retrieve()
                .bodyToMono(String.class)
                .block();
    }

    public String translateArabeToDarija(String text) {
        //  Appel au Model traducteur de l'arabe au darija
        return webClient.post()
                .uri("/translate/arabe-to-darija")
                .bodyValue(text)
                .retrieve()
                .bodyToMono(String.class)
                .block();
    }

}