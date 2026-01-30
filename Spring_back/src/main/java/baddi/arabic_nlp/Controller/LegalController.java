package baddi.arabic_nlp.Controller;

import baddi.arabic_nlp.Services.LegalSimplificationOrchestrator;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
@RequestMapping("/api/legal")
@CrossOrigin(origins = "http://localhost:4200") // Autorise le Front-end Angular
public class LegalController {

    private final LegalSimplificationOrchestrator orchestrator;

    public LegalController(LegalSimplificationOrchestrator orchestrator) {
        this.orchestrator = orchestrator;
    }

    @PostMapping("/ask")
    public Map<String, String> handleQuery(@RequestBody Map<String, String> request) {
        //  Réception du prompt saisi
        String userPrompt = request.get("prompt");

        //  Traitement complet via l'orchestrateur
        String resultInDarija = orchestrator.processLegalQuery(userPrompt);

        //  Retour de la réponse en Darija au Front-end
        return Map.of("simplifiedResponse", resultInDarija);
    }

}