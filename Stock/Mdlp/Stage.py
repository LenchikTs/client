# -*- coding: utf-8 -*-

# Заголовок будет потом,
# сейчас это "превью"

# стадии обмена с МДЛП,
# как движения ЛСиИМН так и отдельных документов обмена с МДЛП

class CMdlpStage:
    unnecessary = 0 # обмен не нужен
    ready       = 1 # документ готов к обмену
    inProgress  = 2 # обмен начат
    failed      = 3 # обмен закончен с ошибкой
    success     = 4 # обмен закончен успешно

    names = (u'Обмен не нужен',           # 0
             u'Подготовлен к обмену',     # 1
             u'В процессе обмена',        # 2
             u'Обмен закончен с ошибкой', # 3
             u'Обмен закончен успешно',   # 4
            )

    @classmethod
    def text(cls, stage):
        if stage is None:
            return u'не задано'
        if 0<=stage<len(cls.names):
            return cls.names[stage]
        else:
            return u'{%s}' % stage


# docStatus
# Пусть пока тут полежит
############################################################################################
# Наименование статуса     # Тип операции                          # Расшифровка статуса
############################################################################################
# UPLOADING_DOCUMENT       # Загрузка документа                    # Документ загружается
# PROCESSING_DOCUMENT      # Первичная обработка документа         # Документ принят и обрабатывается трансформатором
# CORE_PROCESSING_DOCUMENT # Обработка документа системой          # Документ обработан трансформатором и принят на обработку системой
# CORE_PROCESSED_DOCUMENT  # Подготовка ответа                     # Документ обработан системой и трансформатор подготавливает ответ
# PROCESSED_DOCUMENT       # Документ обработан, ответ подготовлен # Документ обработан трансформатором и готов для загрузки
# FAILED                   # Ошибка обработки                      # Произошла ошибка во время обработки документа
# FAILED_RESULT_READY      # Ошибка обработки, ответ подготовлен   # Произошла ошибка во время обработки документа. Квитанция для документа с информацией о причине сбоя сформирована и может быть получена по request_id
