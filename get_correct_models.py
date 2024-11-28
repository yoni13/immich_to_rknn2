def get_corrected_models():
    # from machine-learning/export/run.py
    models = [
        # "LABSE-Vit-L-14",
        # "XLM-Roberta-Large-Vit-B-16Plus",
        # "XLM-Roberta-Large-Vit-B-32",
        # "XLM-Roberta-Large-Vit-L-14",
        # "RN101::openai",
        # "RN101::yfcc15m",
        # "RN50::cc12m",
        # "RN50::openai",
        # "RN50::yfcc15m",
        # "RN50x16::openai",
        # "RN50x4::openai",
        # "RN50x64::openai",
        # "ViT-B-16-SigLIP-256::webli",
        # "ViT-B-16-SigLIP-384::webli",
        # "ViT-B-16-SigLIP-512::webli",
        # "ViT-B-16-SigLIP-i18n-256::webli",
        # "ViT-B-16-SigLIP::webli",
        # "ViT-B-16-plus-240::laion400m_e31",
        # "ViT-B-16-plus-240::laion400m_e32",
        # "ViT-B-16::laion400m_e31",
        # "ViT-B-16::laion400m_e32",
        # "ViT-B-16::openai",
        # "ViT-B-32::laion2b-s34b-b79k",
        # "ViT-B-32::laion2b_e16",
        # "ViT-B-32::laion400m_e31",
        # "ViT-B-32::laion400m_e32",
        # "ViT-B-32::openai",
        # "ViT-H-14-378-quickgelu::dfn5b",
        # "ViT-H-14-quickgelu::dfn5b",
        # "ViT-L-14-336::openai",
        # #ViT-H-14::laion2b-s32b-b79k",
        # "ViT-L-14-quickgelu::dfn2b",
        # "ViT-L-14::laion2b-s32b-b82k",
        # "ViT-L-14::laion400m_e31",
        # "ViT-L-14::laion400m_e32",
        # "ViT-L-14::openai",
        # "ViT-L-16-SigLIP-256::webli",
        # "ViT-L-16-SigLIP-384::webli",
        # "ViT-SO400M-14-SigLIP-384::webli",
        # "ViT-g-14::laion2b-s12b-b42k",
        # "nllb-clip-base-siglip::mrl",
        # "nllb-clip-base-siglip::v1",
        # "nllb-clip-large-siglip::mrl",
        # "nllb-clip-large-siglip::v1",
        # "xlm-roberta-base-ViT-B-32::laion5b_s13b_b90k",
        # "xlm-roberta-large-ViT-H-14::frozen_laion5b_s13b_b90k",
        
        "buffalo_l",
        "antelopev2",
        "buffalo_s",
        "buffalo_m",
        "buffalo_l_batch",
        "scrfd_34g_gnkps"
    ]

    corrected = []
    urls = []

    for model in models:
        corrected.append(model.replace("::", "__"))
        urls.append(f"https://huggingface.co/immich-app/{model.replace('::', '__')}")
    return corrected, urls
