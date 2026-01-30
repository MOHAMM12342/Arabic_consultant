package baddi.arabic_nlp.Services;
import org.springframework.stereotype.Service;

@Service
public class LegalSimplificationOrchestrator {

    private final TranslationClient translationClient;
    private final RagAugmentationService ragService;
    private final LegalModelClient legalModelClient;

    public LegalSimplificationOrchestrator(TranslationClient tc, RagAugmentationService rs, LegalModelClient lmc) {
        this.translationClient = tc;
        this.ragService = rs;
        this.legalModelClient = lmc;
    }

    public String processLegalQuery(String darijaPrompt) {
        // 1. Traduction de l'entrée Citoyen (Darija -> Arabe)
        String arabicPrompt = translationClient.translateDarijaToArabe(darijaPrompt);

        // 2. RAG : Recherche vectorielle et augmentation
        String augmentedPrompt = ragService.augmentPrompt(arabicPrompt);

        // 3. Inférence : Génération de la réponse juridique
        String classicalArabicResponse = legalModelClient.getLegalResponse(augmentedPrompt);

        // 4. Traduction de la sortie (Arabe -> Darija)
        return translationClient.translateArabeToDarija(classicalArabicResponse);

    }
}