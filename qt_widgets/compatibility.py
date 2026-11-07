class CompatibilityChecker:
    """Проверка совместимости компонентов ПК"""

    @staticmethod
    def _parse_number(text):
        """Извлекает первое число из строки (например '220W' -> 220)"""
        if isinstance(text, (int, float)):
            return text
        if not text:
            return 0
        result = ""
        for ch in str(text):
            if ch.isdigit():
                result += ch
            elif result:
                break
        return int(result) if result else 0

    @staticmethod
    def check_compatibility(components):
        """
        Проверяет совместимость выбранных компонентов.
        components: словарь {type: {data}}
        Возвращает список проблем.
        """
        issues = []

        cpu = components.get("cpu")
        mat = components.get("mat")
        ram = components.get("ram")
        cooling = components.get("cooling")
        pb = components.get("pb")
        gpu = components.get("gpu")
        case = components.get("case")

        if cpu and mat:
            cpu_socket = cpu.get("socket", "")
            mat_socket = mat.get("socket", "")
            if cpu_socket and mat_socket and cpu_socket != mat_socket:
                issues.append(
                    {
                        "type": "error",
                        "message": f"Несовместимость сокетов: "
                        f"CPU ({cpu_socket}) ≠ Мат. плата ({mat_socket})",
                        "components": ["cpu", "mat"],
                    }
                )

        if ram and mat:
            ram_type = ram.get("memory_type", "")
            mat_ram = mat.get("memory_slots", "")
            if ram_type and mat_ram and ram_type not in str(mat_ram):
                issues.append(
                    {
                        "type": "error",
                        "message": f"RAM ({ram_type}) "
                        f"не поддерживается матплатой ({mat_ram})",
                        "components": ["ram", "mat"],
                    }
                )

        if cooling and cpu:
            cooling_power = CompatibilityChecker._parse_number(
                cooling.get("power", "")
            )
            cpu_tdp = cpu.get("tdp", 0)
            if cooling_power and cpu_tdp and cooling_power < cpu_tdp:
                issues.append(
                    {
                        "type": "warning",
                        "message": f"Охлаждение слабовато:"
                        f" кулер ({cooling_power}W) < CPU ({cpu_tdp}W)",
                        "components": ["cooling", "cpu"],
                    }
                )

        if pb:
            psu_wattage = pb.get("power", 0)
            total_tdp = 0
            if cpu:
                total_tdp += cpu.get("tdp", 0)
            if gpu:
                # total_tdp += gpu.get("tdp", 0)
                pass
            total_tdp += 100

            if psu_wattage and total_tdp > psu_wattage:
                issues.append(
                    {
                        "type": "error",
                        "message": f"БП слишком слабый: "
                        f"нужно ~{total_tdp}W, есть {psu_wattage}W",
                        "components": ["pb"],
                    }
                )

        if case and mat:
            case_formats = case.get("form-factors", "")
            mat_format = mat.get("form_factor", "")
            if case_formats and mat_format and (
                mat_format not in str(case_formats)
            ):
                issues.append(
                    {
                        "type": "error",
                        "message": f"Мат. плата ({mat_format}) "
                        f"не помещается в корпус ({case_formats})",
                        "components": ["case", "mat"],
                    }
                )

        return issues

    @staticmethod
    def calculate_total_price(components):
        """Подсчитывает общую стоимость сборки"""
        total = 0
        for comp_data in components.values():
            if comp_data and isinstance(comp_data, dict):
                total += comp_data.get("price", 0)
        return total
